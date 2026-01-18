"""
Functional signature and interface validation for medical_extractor.py
Tests the function signatures without requiring GEMINI_API_KEY
"""

import inspect
import asyncio
import sys
import os


def test_function_signatures():
    """Test that functions have correct signatures and type hints"""
    print("\n" + "="*70)
    print("TEST: Function Signatures and Type Hints")
    print("="*70)
    
    # Set dummy API key to avoid configuration error
    os.environ['GEMINI_API_KEY'] = 'test_key_for_signature_check'
    
    try:
        # Import the module
        sys.path.insert(0, '/workspaces/hackathon/UottawaHack/utils')
        from medical_extractor import MedicalDataExtractor
        
        # Test validate_medical_document
        validate_sig = inspect.signature(MedicalDataExtractor.validate_medical_document)
        print("\n✅ validate_medical_document function found")
        print(f"   Signature: {validate_sig}")
        
        # Check parameters
        params = list(validate_sig.parameters.keys())
        if 'file_path' in params:
            print(f"   ✅ Required parameter 'file_path' present")
            param = validate_sig.parameters['file_path']
            if param.annotation != inspect.Parameter.empty:
                print(f"   ✅ Parameter type hint: {param.annotation}")
        else:
            print(f"   ❌ Missing 'file_path' parameter")
        
        # Check return type
        if validate_sig.return_annotation != inspect.Parameter.empty:
            print(f"   ✅ Return type hint: {validate_sig.return_annotation}")
        else:
            print(f"   ⚠️  No return type hint")
        
        # Check if it's async
        if inspect.iscoroutinefunction(MedicalDataExtractor.validate_medical_document):
            print(f"   ✅ Function is async (coroutine)")
        else:
            print(f"   ❌ Function is not async")
        
        # Test extract_patient_data
        extract_sig = inspect.signature(MedicalDataExtractor.extract_patient_data)
        print("\n✅ extract_patient_data function found")
        print(f"   Signature: {extract_sig}")
        
        # Check parameters
        params = list(extract_sig.parameters.keys())
        if 'file_path' in params:
            print(f"   ✅ Required parameter 'file_path' present")
            param = extract_sig.parameters['file_path']
            if param.annotation != inspect.Parameter.empty:
                print(f"   ✅ Parameter type hint: {param.annotation}")
        else:
            print(f"   ❌ Missing 'file_path' parameter")
        
        # Check return type
        if extract_sig.return_annotation != inspect.Parameter.empty:
            print(f"   ✅ Return type hint: {extract_sig.return_annotation}")
        else:
            print(f"   ⚠️  No return type hint")
        
        # Check if it's async
        if inspect.iscoroutinefunction(MedicalDataExtractor.extract_patient_data):
            print(f"   ✅ Function is async (coroutine)")
        else:
            print(f"   ❌ Function is not async")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking function signatures: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_backward_compatibility():
    """Test that module-level functions are available for backward compatibility"""
    print("\n" + "="*70)
    print("TEST: Backward Compatibility Functions")
    print("="*70)
    
    os.environ['GEMINI_API_KEY'] = 'test_key_for_compat_check'
    
    try:
        # Import the module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "medical_extractor",
            "/workspaces/hackathon/UottawaHack/utils/medical_extractor.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Check for module-level functions
        has_extract = hasattr(module, 'extract_patient_data')
        has_validate = hasattr(module, 'validate_medical_document')
        
        if has_extract:
            print("✅ extract_patient_data is available at module level")
        else:
            print("⚠️  extract_patient_data not available at module level")
        
        if has_validate:
            print("✅ validate_medical_document is available at module level")
        else:
            print("⚠️  validate_medical_document not available at module level")
        
        return has_extract and has_validate
        
    except Exception as e:
        print(f"❌ Error checking backward compatibility: {type(e).__name__}: {str(e)}")
        return False


def test_error_handling():
    """Test that functions have proper error handling"""
    print("\n" + "="*70)
    print("TEST: Error Handling and Return Types")
    print("="*70)
    
    os.environ['GEMINI_API_KEY'] = 'test_key_for_error_check'
    
    try:
        sys.path.insert(0, '/workspaces/hackathon/UottawaHack/utils')
        from medical_extractor import MedicalDataExtractor
        
        # Read the source code to check for error handling
        import inspect
        
        validate_source = inspect.getsource(MedicalDataExtractor.validate_medical_document)
        extract_source = inspect.getsource(MedicalDataExtractor.extract_patient_data)
        
        # Check for try-except blocks
        print("\n✅ Checking error handling patterns...")
        
        validate_has_try = 'try:' in validate_source and 'except' in validate_source
        print(f"{'✅' if validate_has_try else '⚠️'} validate_medical_document has try-except blocks: {validate_has_try}")
        
        extract_has_try = 'try:' in extract_source and 'except' in extract_source
        print(f"{'✅' if extract_has_try else '⚠️'} extract_patient_data has try-except blocks: {extract_has_try}")
        
        # Check for return statements
        validate_has_return = 'return' in validate_source
        print(f"{'✅' if validate_has_return else '❌'} validate_medical_document has return statements: {validate_has_return}")
        
        extract_has_return = 'return' in extract_source
        print(f"{'✅' if extract_has_return else '❌'} extract_patient_data has return statements: {extract_has_return}")
        
        # Check for docstrings
        validate_has_doc = MedicalDataExtractor.validate_medical_document.__doc__ is not None
        print(f"{'✅' if validate_has_doc else '⚠️'} validate_medical_document has docstring: {validate_has_doc}")
        
        extract_has_doc = MedicalDataExtractor.extract_patient_data.__doc__ is not None
        print(f"{'✅' if extract_has_doc else '⚠️'} extract_patient_data has docstring: {extract_has_doc}")
        
        return all([validate_has_try, extract_has_try, validate_has_return, extract_has_return])
        
    except Exception as e:
        print(f"❌ Error checking error handling: {type(e).__name__}: {str(e)}")
        return False


def main():
    """Run all function validation tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  MEDICAL EXTRACTOR FUNCTION VALIDATION SUITE".center(68) + "║")
    print("║" + "  (Signature and Interface Testing)".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {
        'function_signatures': test_function_signatures(),
        'backward_compatibility': test_backward_compatibility(),
        'error_handling': test_error_handling(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("FUNCTION VALIDATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        test_label = test_name.replace('_', ' ').title()
        print(f"{test_label:.<45} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL FUNCTION VALIDATION TESTS PASSED!")
    else:
        print("⚠️  SOME VALIDATION TESTS FAILED")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    main()
