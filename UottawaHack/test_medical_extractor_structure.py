"""
Code structure and syntax validation for medical_extractor.py
This test validates the module without requiring GEMINI_API_KEY
"""

import ast
import sys
import os
from pathlib import Path


def test_syntax():
    """Test that the medical_extractor.py has valid Python syntax"""
    print("\n" + "="*70)
    print("TEST 1: Python Syntax Validation")
    print("="*70)
    
    file_path = os.path.join(
        os.path.dirname(__file__),
        'utils',
        'medical_extractor.py'
    )
    
    print(f"\nChecking: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        ast.parse(code)
        print("✅ Python syntax is VALID")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax Error at line {e.lineno}: {e.msg}")
        print(f"   {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_imports():
    """Test that required modules can be imported"""
    print("\n" + "="*70)
    print("TEST 2: Required Imports Availability")
    print("="*70)
    
    required_modules = {
        'google.generativeai': 'Google Generative AI SDK',
        'json': 'JSON module (built-in)',
        'os': 'OS module (built-in)',
        'typing': 'Typing module (built-in)',
        'dotenv': 'Python-dotenv',
    }
    
    all_available = True
    
    for module_name, description in required_modules.items():
        try:
            __import__(module_name)
            print(f"✅ {description:.<40} Available")
        except ImportError as e:
            print(f"❌ {description:.<40} MISSING")
            all_available = False
    
    return all_available


def test_class_structure():
    """Test that MedicalDataExtractor class is properly defined"""
    print("\n" + "="*70)
    print("TEST 3: Class Structure Validation")
    print("="*70)
    
    file_path = os.path.join(
        os.path.dirname(__file__),
        'utils',
        'medical_extractor.py'
    )
    
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        # Find the class definition
        class_found = False
        methods = []
        constants = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'MedicalDataExtractor':
                class_found = True
                
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                constants.append(target.id)
        
        if not class_found:
            print("❌ MedicalDataExtractor class not found")
            return False
        
        print("✅ MedicalDataExtractor class found")
        
        # Check for required methods
        required_methods = [
            'validate_medical_document',
            'extract_patient_data'
        ]
        
        missing_methods = [m for m in required_methods if m not in methods]
        
        if missing_methods:
            print(f"❌ Missing methods: {', '.join(missing_methods)}")
            return False
        
        print(f"✅ All required methods found: {', '.join(required_methods)}")
        
        # Check for required constants
        if 'DOCUMENT_TYPES' not in constants:
            print("❌ DOCUMENT_TYPES constant not found")
            return False
        
        print("✅ DOCUMENT_TYPES constant found")
        
        if 'EXTRACTION_PROMPT' not in constants:
            print("❌ EXTRACTION_PROMPT constant not found")
            return False
        
        print("✅ EXTRACTION_PROMPT constant found")
        
        print(f"\nClass Details:")
        print(f"  - Methods: {len(methods)} total")
        print(f"    {', '.join(methods)}")
        print(f"  - Constants/Class variables: {len(constants)} total")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing class structure: {type(e).__name__}: {str(e)}")
        return False


def test_document_types():
    """Test that DOCUMENT_TYPES dictionary is properly populated"""
    print("\n" + "="*70)
    print("TEST 4: Document Types Dictionary Validation")
    print("="*70)
    
    file_path = os.path.join(
        os.path.dirname(__file__),
        'utils',
        'medical_extractor.py'
    )
    
    try:
        # Import the module dynamically (without API key)
        import importlib.util
        spec = importlib.util.spec_from_file_location("medical_extractor", file_path)
        module = importlib.util.module_from_spec(spec)
        
        # Suppress Gemini API key error by setting a dummy one
        os.environ['GEMINI_API_KEY'] = 'test_key_for_syntax_check'
        
        spec.loader.exec_module(module)
        
        doc_types = module.MedicalDataExtractor.DOCUMENT_TYPES
        
        print(f"✅ DOCUMENT_TYPES loaded successfully")
        print(f"✅ Total document types defined: {len(doc_types)}")
        
        # Sample some categories
        categories = {
            'Primary Care': ['annual_physical', 'general_practitioner_notes', 'office_visit_note'],
            'Lab Results': ['blood_test_results', 'urinalysis', 'cholesterol_panel'],
            'Imaging': ['chest_xray_report', 'ct_scan_report', 'mri_scan_report'],
            'Medications': ['prescription_receipt', 'pharmacy_receipt', 'medication_list'],
        }
        
        all_present = True
        for category, expected_types in categories.items():
            present = [t for t in expected_types if t in doc_types]
            if len(present) == len(expected_types):
                print(f"  ✅ {category}: All {len(expected_types)} types present")
            else:
                print(f"  ⚠️  {category}: {len(present)}/{len(expected_types)} types present")
                missing = [t for t in expected_types if t not in doc_types]
                if missing:
                    print(f"      Missing: {', '.join(missing)}")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error validating document types: {type(e).__name__}: {str(e)}")
        return False


def test_prompts():
    """Test that extraction prompts are properly defined"""
    print("\n" + "="*70)
    print("TEST 5: Extraction Prompt Validation")
    print("="*70)
    
    file_path = os.path.join(
        os.path.dirname(__file__),
        'utils',
        'medical_extractor.py'
    )
    
    try:
        import importlib.util
        
        # Suppress Gemini API key error
        os.environ['GEMINI_API_KEY'] = 'test_key_for_syntax_check'
        
        spec = importlib.util.spec_from_file_location("medical_extractor", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        prompt = module.MedicalDataExtractor.EXTRACTION_PROMPT
        
        print(f"✅ EXTRACTION_PROMPT loaded successfully")
        print(f"✅ Prompt length: {len(prompt)} characters")
        
        # Check for key instruction components
        required_keywords = [
            'JSON',
            'age',
            'gender',
            'conditions',
            'medications',
            'document_type',
            'confidence_score',
            'lab_results',
            'allergies'
        ]
        
        missing_keywords = []
        for keyword in required_keywords:
            if keyword not in prompt:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            print(f"⚠️  Missing keywords in prompt: {', '.join(missing_keywords)}")
            return False
        else:
            print(f"✅ All required keywords present in prompt")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating prompts: {type(e).__name__}: {str(e)}")
        return False


def test_sample_pdf():
    """Test that sample PDF exists"""
    print("\n" + "="*70)
    print("TEST 6: Sample PDF Availability")
    print("="*70)
    
    sample_pdf_path = os.path.join(
        os.path.dirname(__file__),
        'sample_pdfs',
        'patient_a_medical_record.pdf'
    )
    
    if os.path.exists(sample_pdf_path):
        file_size = os.path.getsize(sample_pdf_path)
        print(f"✅ Sample PDF found: {sample_pdf_path}")
        print(f"✅ File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        return True
    else:
        print(f"❌ Sample PDF not found at: {sample_pdf_path}")
        return False


def main():
    """Run all structure and syntax tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  MEDICAL EXTRACTOR CODE VALIDATION SUITE".center(68) + "║")
    print("║" + "  (No GEMINI_API_KEY required)".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {
        'syntax': test_syntax(),
        'imports': test_imports(),
        'class_structure': test_class_structure(),
        'document_types': test_document_types(),
        'prompts': test_prompts(),
        'sample_pdf': test_sample_pdf(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("CODE VALIDATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        test_label = test_name.replace('_', ' ').title()
        print(f"{test_label:.<45} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL CODE VALIDATION TESTS PASSED!")
        print("\n📋 To run functional tests with API:")
        print("   1. Get API key: https://aistudio.google.com/app/apikey")
        print("   2. Create .env file with: GEMINI_API_KEY=your_key")
        print("   3. Run: python test_medical_extractor.py")
    else:
        print("⚠️  SOME VALIDATION TESTS FAILED")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    main()
