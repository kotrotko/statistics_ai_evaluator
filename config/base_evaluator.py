"""
Base evaluator class for all question graders_hw5.

This module provides the BaseEvaluator class that contains common functionality
shared across all question evaluators including API communication, JSON parsing,
error handling, and result validation.
"""

import re
import json
from typing import Dict, Any, Optional
from .api_handler import GroqAPIHandler


class BaseEvaluator:
    """
    Base class for all question evaluators.

    Provides common functionality for:
    - Groq API initialization (via GroqAPIHandler)
    - API calls with error handling
    - JSON response parsing
    - Result validation
    - Safety check enforcement

    Attributes:
        api_handler (GroqAPIHandler): Groq API handler instance
        model (str): Model name to use for grading
        temperature (float): Temperature setting for API calls
        max_tokens (int): Maximum tokens for responses
    """

    def __init__(self, model: str = "openai/gpt-oss-120b",
                 temperature: float = 0.3,
                 max_tokens: int = 2000,
                 reasoning_effort: str = "low"):
        """
        Initialize the base evaluator.

        Args:
            model: Groq model name to use
            temperature: Temperature for API calls (0.0-1.0)
            max_tokens: Maximum tokens for response
            reasoning_effort: Reasoning depth for gpt-oss models ('low', 'medium', 'high')

        Raises:
            ValueError: If GROQ_API_KEY environment variable is not set
        """
        # Use GroqAPIHandler for all API communication
        self.api_handler = GroqAPIHandler(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort
        )

        # Store settings for reference
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        reasoning_effort = reasoning_effort

    def call_groq_api(self, prompt: str) -> str:
        """
        Make an API call to Groq.

        Args:
            prompt: The prompt to send to the API

        Returns:
            Raw response text from the API

        Raises:
            Exception: If API call fails
        """
        try:
            return self.api_handler.create_chat_completion(prompt=prompt)
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")

    def parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from API response, handling markdown code blocks.

        Args:
            response_text: Raw response text from API

        Returns:
            Parsed JSON as dictionary

        Raises:
            json.JSONDecodeError: If JSON parsing fails
        """
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

        return json.loads(json_str)

    def validate_component_scores(self, result: Dict[str, Any],
                                  component_keys: list,
                                  max_points: int) -> Dict[str, Any]:
        """
        Validate that component scores sum to total_points.

        Args:
            result: Grading result dictionary
            component_keys: List of component score keys to sum
            max_points: Maximum possible points

        Returns:
            Updated result dictionary with corrected totals
        """
        if all(key in result for key in component_keys):
            calculated_total = sum(result[key] for key in component_keys)
            result['total_points'] = calculated_total
            result['max_points'] = max_points
            result['percentage'] = round((calculated_total / max_points) * 100, 1)

        return result

    def enforce_safety_check(self, result: Dict[str, Any],
                             check_result: Dict[str, Any],
                             component_key: str,
                             base_score: int,
                             penalty_key: str = 'penalty') -> Dict[str, Any]:
        """
        Enforce automatic penalty/safety checks on component scores.

        This method ensures that automatic checks (like SD removal, extra statistics)
        are properly enforced even if the AI model misses them.

        Args:
            result: Grading result dictionary
            check_result: Detection check result (e.g., from check_sd_removed)
            component_key: Key for the component to apply penalty to
            base_score: Base score before penalty
            penalty_key: Key in check_result containing penalty value

        Returns:
            Updated result dictionary with enforced penalty
        """
        if check_result.get(penalty_key, 0) > 0:
            penalty = check_result[penalty_key]
            corrected_score = max(0, base_score - penalty)

            if result.get(component_key, 0) > corrected_score:
                print(f"\n⚠️  WARNING: AI gave {result[component_key]} points for {component_key} "
                      f"despite {penalty} point penalty. Correcting to {corrected_score}.")
                result[component_key] = corrected_score

        return result

    def grade_with_prompt(self, student_answer: str,
                          prompt: str,
                          additional_checks: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Standard grading workflow: API call -> parse -> validate.

        Args:
            student_answer: The student's response text
            prompt: Grading prompt to send to API
            additional_checks: Optional dictionary of check results to include

        Returns:
            Grading result dictionary with scores and feedback
        """
        try:
            # Call API
            response_text = self.call_groq_api(prompt)

            print(f"RAW_LEN={len(response_text)} RAW_HEAD={response_text[:80]!r} RAW_TAIL={response_text[-80:]!r}")

            # Parse JSON
            result = self.parse_json_response(response_text)

            # Add additional checks if provided
            if additional_checks:
                result.update(additional_checks)

            return result

        except json.JSONDecodeError as e:
            return {
                "error": "Could not parse grading result",
                "raw_response": response_text if 'response_text' in locals() else None,
                "parse_error": str(e),
                **(additional_checks or {})
            }
        except Exception as e:
            return {
                "error": "Grading failed",
                "error_message": str(e),
                **(additional_checks or {})
            }

    def create_mock_result(self, component_scores: Dict[str, int],
                           max_points: int,
                           feedback: str,
                           vibe: str,
                           additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a mock test result for testing without API calls.

        Args:
            component_scores: Dictionary of component names to scores
            max_points: Maximum possible points
            feedback: Feedback text
            vibe: Overall vibe/impression text
            additional_data: Optional additional data to include

        Returns:
            Mock grading result dictionary
        """
        total = sum(component_scores.values())
        percentage = round((total / max_points) * 100, 1)

        result = {
            **component_scores,
            "total_points": total,
            "max_points": max_points,
            "percentage": percentage,
            "feedback": f"[TEST MODE] {feedback}",
            "vibe": vibe
        }

        if additional_data:
            result.update(additional_data)

        return result