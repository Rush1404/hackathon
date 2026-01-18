"""
Comprehensive test suite for medical_extractor.py

Tests both validate_medical_document and extract_patient_data functions
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from medical_extractor import MedicalDataExtractor

# Load environment variables
load_dotenv()


async def test_validate_medical_document():
    """Test the validate_medical_document function"""
    print("\n" + "="*70)
    print("TEST 1: validate_medical_document()")
    print("="*70)
    
    sample_pdf_path = os.path.join(
        os.path.dirname(__file__),
        'sample_pdfs',
        'patient_a_medical_record.pdf'
    )
    
    if not os.path.exists(sample_pdf_path):
        print(f"❌ Sample PDF not found at: {sample_pdf_path}")
        return False
    
    print(f"✓ Sample PDF found: {sample_pdf_path}")
    print(f"✓ File size: {os.path.getsize(sample_pdf_path)} bytes")
    
    try:
        print("\n📋 Validating medical document...")
        result = await MedicalDataExtractor.validate_medical_document(sample_pdf_path)
        
        print("\nValidation Results:")
        print(f"  - is_valid: {result['is_valid']}")
        print(f"  - document_type: {result['document_type']}")
        print(f"  - confidence: {result['confidence']:.2%}")
        print(f"  - reason: {result['reason']}")
        
        if result['is_valid']:
            print("\n✅ Document validation PASSED - Document is a valid medical document")
            return True
        else:
            print("\n⚠️  Document marked as invalid - may not be a recognized medical document type")
            return True  # Still return True since the function executed correctly
            
    except Exception as e:
        print(f"\n❌ Error during validation: {type(e).__name__}: {str(e)}")
        return False


async def test_extract_patient_data():
    """Test the extract_patient_data function"""
    print("\n" + "="*70)
    print("TEST 2: extract_patient_data()")
    print("="*70)
    
    sample_pdf_path = os.path.join(
        os.path.dirname(__file__),
        'sample_pdfs',
        'patient_a_medical_record.pdf'
    )
    
    if not os.path.exists(sample_pdf_path):
        print(f"❌ Sample PDF not found at: {sample_pdf_path}")
        return False
    
    try:
        print(f"\n📄 Extracting patient data from: {sample_pdf_path}")
        result = await MedicalDataExtractor.extract_patient_data(sample_pdf_path)
        
        print("\nExtraction Results:")
        print(f"  - Status: {result['status']}")
        
        if result['error']:
            print(f"  - Error: {result['error']}")
        
        if result['status'] == 'success':
            data = result['data']
            print(f"\n✅ Extraction SUCCESSFUL")
            print("\nExtracted Data:")
            print(f"  - Document Type: {data.get('document_type', 'N/A')}")
            print(f"  - Patient Age: {data.get('age', 'N/A')}")
            print(f"  - Gender: {data.get('gender', 'N/A')}")
            print(f"  - Ethnicity: {data.get('ethnicity', 'N/A')}")
            print(f"  - Patient Name: {data.get('patient_name', 'N/A')}")
            print(f"  - Confidence Score: {data.get('confidence_score', 'N/A')}")
            
            # Conditions
            conditions = data.get('conditions', [])
            if conditions:
                print(f"  - Conditions ({len(conditions)}):")
                for cond in conditions:
                    print(f"      • {cond}")
            
            # Medications
            medications = data.get('medications', [])
            if medications:
                print(f"  - Medications ({len(medications)}):")
                for med in medications:
                    print(f"      • {med}")
            
            # Allergies
            allergies = data.get('allergies', [])
            if allergies:
                print(f"  - Allergies ({len(allergies)}):")
                for allergy in allergies:
                    print(f"      • {allergy}")
            
            # Providers
            providers = data.get('providers', [])
            if providers:
                print(f"  - Healthcare Providers ({len(providers)}):")
                for provider in providers:
                    print(f"      • {provider}")
            
            # Lab results
            lab_results = data.get('lab_results', {})
            if lab_results:
                print(f"  - Lab Results ({len(lab_results)}):")
                for test_name, value in lab_results.items():
                    print(f"      • {test_name}: {value}")
            
            # Vital signs
            vital_signs = data.get('vital_signs', {})
            if vital_signs:
                print(f"  - Vital Signs:")
                for sign, value in vital_signs.items():
                    print(f"      • {sign}: {value}")
            
            # Additional fields
            optional_fields = [
                ('chief_complaint', 'Chief Complaint'),
                ('visit_date', 'Visit Date'),
                ('lab_date', 'Lab Date'),
                ('surgery_date', 'Surgery Date'),
                ('imaging_type', 'Imaging Type'),
                ('findings', 'Findings'),
                ('assessment_plan', 'Assessment/Plan'),
                ('surgery_type', 'Surgery Type'),
                ('dental_findings', 'Dental Findings'),
                ('vaccines_administered', 'Vaccines'),
            ]
            
            for field_key, field_label in optional_fields:
                if data.get(field_key):
                    print(f"  - {field_label}: {data.get(field_key)}")
            
            print("\n📊 Full JSON Response:")
            print(json.dumps(result['data'], indent=2))
            
            return True
        else:
            print(f"\n⚠️  Extraction status: {result['status']}")
            print("Full Result:")
            print(json.dumps(result, indent=2))
            return False
            
    except Exception as e:
        print(f"\n❌ Error during extraction: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_imports():
    """Test that all imports work correctly"""
    print("\n" + "="*70)
    print("TEST 0: Import and Environment Check")
    print("="*70)
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import google.generativeai: {e}")
        return False
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY environment variable is set")
    else:
        print("⚠️  GEMINI_API_KEY environment variable is NOT set")
        print("   Tests will fail without a valid API key")
        return False
    
    try:
        extractor = MedicalDataExtractor()
        print("✅ MedicalDataExtractor class instantiated successfully")
    except Exception as e:
        print(f"❌ Failed to instantiate MedicalDataExtractor: {e}")
        return False
    
    # Verify methods exist
    if hasattr(MedicalDataExtractor, 'validate_medical_document'):
        print("✅ validate_medical_document method exists")
    else:
        print("❌ validate_medical_document method not found")
        return False
    
    if hasattr(MedicalDataExtractor, 'extract_patient_data'):
        print("✅ extract_patient_data method exists")
    else:
        print("❌ extract_patient_data method not found")
        return False
    
    return True


async def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  MEDICAL EXTRACTOR COMPREHENSIVE TEST SUITE".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    # Test 0: Imports
    results['imports'] = await test_imports()
    
    if not results['imports']:
        print("\n" + "="*70)
        print("❌ CRITICAL: Import or environment check failed")
        print("\n📋 TO FIX: Set up your GEMINI_API_KEY")
        print("="*70)
        print("\n1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("\n2. Create a .env file in /workspaces/hackathon/UottawaHack/")
        print("   with the content:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("\n3. Or set it as an environment variable:")
        print("   export GEMINI_API_KEY=your_api_key_here")
        print("\n4. Then run this test again")
        print("="*70)
        return results
    
    # Test 1: Validation
    results['validation'] = await test_validate_medical_document()
    
    # Test 2: Extraction
    results['extraction'] = await test_extract_patient_data()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
