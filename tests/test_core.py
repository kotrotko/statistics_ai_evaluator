"""
Test script to validate all config modules work correctly.

This script tests each config module independently to ensure
everything is working before refactoring evaluators.
"""

import sys
import os

# tests/ and classwork_1/ are siblings
# Go up from tests/ to AIAgent/, then into classwork_1/
current_dir = os.path.dirname(os.path.abspath(__file__))  # tests/
parent_dir = os.path.dirname(current_dir)                  # AIAgent/
classwork_dir = os.path.join(parent_dir, 'classwork_1')   # AIAgent/classwork_1/
sys.path.insert(0, classwork_dir)

def print_test_header(test_name):
    """Print formatted test header."""
    print("\n" + "=" * 60)
    print(f"TEST: {test_name}")
    print("=" * 60)


def print_result(passed, message):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")


def test_1_imports():
    """Test 1: Can we import all config modules?"""
    print_test_header("Core Module Imports")

    tests_passed = 0
    tests_total = 5

    # Test __init__.py
    try:
        import core
        print_result(True, "config package imported")
        tests_passed += 1
    except Exception as e:
        print_result(False, f"config package import failed: {e}")

    # Test base_evaluator.py
    try:
        from core.base_evaluator import BaseEvaluator
        print_result(True, "BaseEvaluator imported")
        tests_passed += 1
    except Exception as e:
        print_result(False, f"BaseEvaluator import failed: {e}")

    # Test api_handler.py
    try:
        from core.api_handler import GroqAPIHandler, test_groq_connection
        print_result(True, "GroqAPIHandler imported")
        tests_passed += 1
    except Exception as e:
        print_result(False, f"GroqAPIHandler import failed: {e}")

    # Test input_handler.py
    try:
        from core.input_handler import get_student_input, prompt_for_input
        print_result(True, "input_handler functions imported")
        tests_passed += 1
    except Exception as e:
        print_result(False, f"input_handler import failed: {e}")

    # Test output_formatter.py
    try:
        from core.output_formatter import print_grading_results, print_header
        print_result(True, "output_formatter functions imported")
        tests_passed += 1
    except Exception as e:
        print_result(False, f"output_formatter import failed: {e}")

    return tests_passed, tests_total


def test_2_api_connection():
    """Test 2: Can we connect to Groq API?"""
    print_test_header("Groq API Connection")

    # Check if API key is set
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print_result(False, "GROQ_API_KEY environment variable not set")
        print("  → Please set GROQ_API_KEY before running tests")
        return 0, 1

    print_result(True, "GROQ_API_KEY is set")

    # Test connection
    try:
        from core.api_handler import test_groq_connection

        print("  Testing API connection (this may take a few seconds)...")
        connected = test_groq_connection()

        if connected:
            print_result(True, "Groq API connection successful")
            return 1, 1
        else:
            print_result(False, "Groq API connection failed")
            return 0, 1
    except Exception as e:
        print_result(False, f"API connection test error: {e}")
        return 0, 1


def test_3_base_evaluator():
    """Test 3: Can we create a BaseEvaluator instance?"""
    print_test_header("BaseEvaluator Instantiation")

    try:
        from core.base_evaluator import BaseEvaluator

        evaluator = BaseEvaluator()
        print_result(True, "BaseEvaluator instance created")

        # Check if it has expected methods
        has_methods = all([
            hasattr(evaluator, 'call_groq_api'),
            hasattr(evaluator, 'parse_json_response'),
            hasattr(evaluator, 'validate_component_scores'),
            hasattr(evaluator, 'enforce_safety_check'),
            hasattr(evaluator, 'grade_with_prompt'),
            hasattr(evaluator, 'create_mock_result')
        ])

        if has_methods:
            print_result(True, "All expected methods present")
            return 2, 2
        else:
            print_result(False, "Some methods missing")
            return 1, 2

    except Exception as e:
        print_result(False, f"BaseEvaluator creation failed: {e}")
        return 0, 2


def test_4_json_parsing():
    """Test 4: Can we parse JSON responses?"""
    print_test_header("JSON Response Parsing")

    try:
        from core.base_evaluator import BaseEvaluator

        evaluator = BaseEvaluator()

        # Test with markdown JSON
        markdown_response = '''
Here is the result:
```json
{
  "score": 95,
  "feedback": "Great work!"
}
```
'''
        result = evaluator.parse_json_response(markdown_response)

        if result.get('score') == 95:
            print_result(True, "Parsed markdown-wrapped JSON correctly")
        else:
            print_result(False, "Markdown JSON parsing failed")
            return 0, 2

        # Test with plain JSON
        plain_response = '{"score": 85, "feedback": "Good"}'
        result = evaluator.parse_json_response(plain_response)

        if result.get('score') == 85:
            print_result(True, "Parsed plain JSON correctly")
            return 2, 2
        else:
            print_result(False, "Plain JSON parsing failed")
            return 1, 2

    except Exception as e:
        print_result(False, f"JSON parsing test failed: {e}")
        return 0, 2


def test_5_validation():
    """Test 5: Does component score validation work?"""
    print_test_header("Component Score Validation")

    try:
        from core.base_evaluator import BaseEvaluator

        evaluator = BaseEvaluator()

        # Test data
        result = {
            "component_1_score": 5,
            "component_2_score": 4,
            "component_3_score": 5
        }

        component_keys = ["component_1_score", "component_2_score", "component_3_score"]

        validated = evaluator.validate_component_scores(result, component_keys, 15)

        checks_passed = 0

        if validated.get('total_points') == 14:
            print_result(True, "Total points calculated correctly (14)")
            checks_passed += 1
        else:
            print_result(False, f"Total points wrong: {validated.get('total_points')}")

        if validated.get('percentage') == 93.3:
            print_result(True, "Percentage calculated correctly (93.3%)")
            checks_passed += 1
        else:
            print_result(False, f"Percentage wrong: {validated.get('percentage')}")

        return checks_passed, 2

    except Exception as e:
        print_result(False, f"Validation test failed: {e}")
        return 0, 2


def test_6_mock_result():
    """Test 6: Can we create mock results?"""
    print_test_header("Mock Result Creation")

    try:
        from core.base_evaluator import BaseEvaluator

        evaluator = BaseEvaluator()

        mock = evaluator.create_mock_result(
            component_scores={"component_1_score": 5, "component_2_score": 4},
            max_points=10,
            feedback="Test feedback",
            vibe="Test vibe"
        )

        checks_passed = 0

        if mock.get('total_points') == 9:
            print_result(True, "Mock total calculated correctly")
            checks_passed += 1
        else:
            print_result(False, f"Mock total wrong: {mock.get('total_points')}")

        if "[TEST MODE]" in mock.get('feedback', ''):
            print_result(True, "Mock feedback marked correctly")
            checks_passed += 1
        else:
            print_result(False, "Mock feedback not marked")

        return checks_passed, 2

    except Exception as e:
        print_result(False, f"Mock result test failed: {e}")
        return 0, 2


def test_7_output_formatting():
    """Test 7: Does output formatting work?"""
    print_test_header("Output Formatting")

    try:
        from core.output_formatter import (
            print_header,
            print_component_breakdown,
            format_grading_report
        )

        # Test header
        print("\n  Testing print_header():")
        print_header("TEST HEADER", width=40)
        print_result(True, "print_header() works")

        # Test component breakdown
        print("\n  Testing print_component_breakdown():")
        test_grading = {
            "component_1_score": 5,
            "component_2_score": 4
        }
        component_labels = {
            "component_1_score": "Component 1",
            "component_2_score": "Component 2"
        }
        print_component_breakdown(test_grading, component_labels)
        print_result(True, "print_component_breakdown() works")

        # Test report formatting
        report = format_grading_report(
            test_grading,
            student_id="test_123",
            question_name="TEST",
            include_timestamp=False
        )

        if "test_123" in report:
            print_result(True, "format_grading_report() works")
            return 3, 3
        else:
            print_result(False, "Report formatting incomplete")
            return 2, 3

    except Exception as e:
        print_result(False, f"Output formatting test failed: {e}")
        return 0, 3


def run_all_tests():
    """Run all validation tests."""
    print("=" * 60)
    print("CORE MODULE VALIDATION TEST SUITE")
    print("=" * 60)
    print("\nThis will test all config/ modules to ensure they work correctly.")
    print("Make sure GROQ_API_KEY is set in your environment.\n")

    total_passed = 0
    total_tests = 0

    # Run all tests
    tests = [
        ("Import Tests", test_1_imports),
        ("API Connection", test_2_api_connection),
        ("BaseEvaluator", test_3_base_evaluator),
        ("JSON Parsing", test_4_json_parsing),
        ("Score Validation", test_5_validation),
        ("Mock Results", test_6_mock_result),
        ("Output Formatting", test_7_output_formatting),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            passed, total = test_func()
            total_passed += passed
            total_tests += total
            results.append((test_name, passed, total))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, 0, 1))
            total_tests += 1

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed, total in results:
        percentage = (passed / total * 100) if total > 0 else 0
        status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
        print(f"{status} {test_name}: {passed}/{total} ({percentage:.0f}%)")

    print("\n" + "=" * 60)
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_percentage:.1f}%)")
    print("=" * 60)

    if total_passed == total_tests:
        print("\n🎉 SUCCESS! All config modules are working correctly.")
        print("You can proceed to Phase 2: Refactoring evaluators.\n")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix issues before proceeding.\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)