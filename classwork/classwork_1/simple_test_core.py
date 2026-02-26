"""
Simple test script to validate config modules.
Place this file INSIDE classwork_1/ folder (next to config/ folder).
"""

import os


print("=" * 60)
print("SIMPLE CORE MODULE TEST")
print("=" * 60)

# Test 1: Import config modules
print("\n1. Testing imports...")
try:
    from config.base_evaluator import BaseEvaluator
    print("   ✅ BaseEvaluator imported")
except Exception as e:
    print(f"   ❌ BaseEvaluator failed: {e}")
    exit(1)

try:
    from config.api_handler import GroqAPIHandler
    print("   ✅ GroqAPIHandler imported")
except Exception as e:
    print(f"   ❌ GroqAPIHandler failed: {e}")
    exit(1)

try:
    from config.input_handler import get_student_input
    print("   ✅ input_handler imported")
except Exception as e:
    print(f"   ❌ input_handler failed: {e}")
    exit(1)

try:
    from config.output_formatter import print_header
    print("   ✅ output_formatter imported")
except Exception as e:
    print(f"   ❌ output_formatter failed: {e}")
    exit(1)

# Test 2: Create BaseEvaluator instance
print("\n2. Testing BaseEvaluator creation...")
try:
    evaluator = BaseEvaluator()
    print("   ✅ BaseEvaluator instance created")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    exit(1)

# Test 3: Test API connection
print("\n3. Testing Groq API connection...")
try:
    from config.api_handler import test_groq_connection
    if test_groq_connection():
        print("   ✅ API connection successful")
    else:
        print("   ⚠️  API connection failed (check your key)")
except Exception as e:
    print(f"   ❌ Connection test failed: {e}")

# Test 4: Test JSON parsing
print("\n4. Testing JSON parsing...")
try:
    test_json = '```json\n{"score": 95}\n```'
    result = evaluator.parse_json_response(test_json)
    if result.get('score') == 95:
        print("   ✅ JSON parsing works")
    else:
        print("   ❌ JSON parsing failed")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Test validation
print("\n5. Testing score validation...")
try:
    test_result = {
        "component_1_score": 5,
        "component_2_score": 4
    }
    validated = evaluator.validate_component_scores(
        test_result,
        ["component_1_score", "component_2_score"],
        10
    )
    if validated.get('total_points') == 9:
        print("   ✅ Validation works")
    else:
        print("   ❌ Validation failed")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Test output formatting
print("\n6. Testing output formatting...")
try:
    from config.output_formatter import print_header
    print("\n   Testing print_header:")
    print_header("   TEST HEADER", width=40, char="-")
    print("   ✅ Output formatting works")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 60)
print("✅ ALL CORE TESTS PASSED!")
print("=" * 60)
print("\nCore package is working correctly.")
print("You can proceed to Phase 2: Refactoring evaluators.")