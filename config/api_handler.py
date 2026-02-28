"""
Shared Groq API configuration for all evaluators.
This module provides a centralized way to manage Groq API credentials.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# This function reads the .env file and loads the variables into your system memory
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Now the code pulls the key from memory, not from the hardcoded text
api_key = os.getenv("GROQ_API_KEY")

# ============================================================================
# FUNCTION-BASED API ACCESS (Simple approach)
# ============================================================================

def get_groq_client() -> Groq:
    """
    Get a configured Groq client instance.

    Returns:
        Groq: Configured Groq client

    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set GROQ_API_KEY environment variable")

    return Groq(api_key=api_key)


def get_api_key() -> str:
    """
    Get the Groq API key.

    Returns:
        str: The API key

    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Please set GROQ_API_KEY environment variable")

    return api_key


# ============================================================================
# CLASS-BASED API HANDLER (For BaseEvaluator)
# ============================================================================

class GroqAPIHandler:
    """
    Handler class for Groq API interactions.

    This class encapsulates all Groq API communication logic including
    client initialization, completion requests, and error handling.

    Attributes:
        model (str): The Groq model to use for completions
        temperature (float): Temperature setting for API calls (0.0-1.0)
        max_tokens (int): Maximum tokens for API responses
    """

    def __init__(self,
                 model: str = "llama-3.3-70b-versatile",
                 temperature: float = 0.3,
                 max_tokens: int = 1200):
        """
        Initialize the Groq API handler.

        Args:
            model: Model name to use for completions
            temperature: Temperature for API calls (0.0-1.0)
            max_tokens: Maximum tokens for responses

        Raises:
            ValueError: If GROQ_API_KEY is not set
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None  # Lazy initialization

    def _get_client(self) -> Groq:
        """
        Internal method to get or create the Groq client.
        Uses lazy initialization - client is only created when first needed.

        Returns:
            Groq: Configured Groq client instance

        Raises:
            ValueError: If GROQ_API_KEY is not set
        """
        if self._client is None:
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                raise ValueError("Please set GROQ_API_KEY environment variable")
            self._client = Groq(api_key=api_key)

        return self._client

    def create_chat_completion(self, prompt: str) -> str:
        """
        Create a chat completion using the Groq API.

        Args:
            prompt: The prompt/message to send to the model

        Returns:
            str: The response text from the model

        Raises:
            Exception: If the API call fails
        """
        try:
            client = self._get_client()

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract and return the response text
            return chat_completion.choices[0].message.content

        except Exception as e:
            raise Exception(f"Groq API call failed: {str(e)}")
