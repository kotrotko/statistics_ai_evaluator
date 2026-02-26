"""
Config package for statistics grading system.
"""

from .base_evaluator import BaseEvaluator
from .api_handler import get_groq_client, get_api_key, GroqAPIHandler
from .input_handler import InputHandler
from .output_formatter import OutputFormatter, print_grading_results

__all__ = [
    # Core classes
    'BaseEvaluator',
    'GroqAPIHandler',
    'InputHandler',
    'OutputFormatter',

    # API utility functions
    'get_groq_client',
    'get_api_key',

    # Backward compatibility functions
    'print_grading_results',
]

__version__ = '1.0.0'
__author__ = 'Statistics Grading System'