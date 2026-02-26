"""
Tests package for statistics grading system.

This package contains test modules for validating the grading system components.

Test Modules:
    - test_core: Validates config package modules (base_evaluator, api_handler, etc.)
    - test_evaluators: Tests individual question evaluators (future)
    - test_integration: End-to-end integration tests (future)

Usage:
    Run all tests:
        python -m pytest tests/

    Run specific test module:
        python -m tests.test_core
        python tests/test_core.py

    Run with coverage:
        python -m pytest tests/ --cov=config --cov=evaluators
"""

__version__ = '1.0.0'
__all__ = ['test_core']
