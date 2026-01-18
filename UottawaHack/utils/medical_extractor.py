"""
Medical PDF Extraction Module
Extracts structured patient data from medical PDFs using Gemini AI
"""

import google.generativeai as genai
import json
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
MODEL_ID = 'gemini-2.0-flash'


class MedicalDataExtractor:
    """Extract structured medical data from PDF documents"""
    
    DOCUMENT_TYPES = {
        # Primary Care & General
        'annual_physical': 'Annual physical exam report and findings',
        'general_practitioner_notes': 'GP visit notes and clinical observations',
        'office_visit_note': 'Primary care office visit documentation',
        'patient_summary': 'Medical summary letter from healthcare provider',
        'health_insurance_form': 'Insurance claim and eligibility forms',
        'referral_letter': 'Referral to specialist or other provider',
        
        # Lab & Test Results
        'blood_test_results': 'General blood test and serology results',
        'urinalysis': 'Urine test results and analysis',
        'cholesterol_panel': 'Lipid panel and cholesterol levels',
        'glucose_test': 'Blood glucose and diabetes screening',
        'complete_blood_count': 'CBC results with cell counts',
        'metabolic_panel': 'Comprehensive metabolic panel (CMP)',
        'thyroid_function_test': 'TSH and thyroid hormone levels',
        'covid_test_result': 'COVID-19 PCR or antigen test result',
        'allergy_test_results': 'Allergy testing and sensitivity results',
        'drug_screening_result': 'Substance screening test results',
        'pregnancy_test_result': 'Pregnancy confirmation test results',
        'coagulation_test': 'PT/INR and blood clotting studies',
        'liver_function_test': 'Liver enzyme and function tests',
        'kidney_function_test': 'Renal function and creatinine levels',
        'testosterone_test': 'Hormone level testing results',
        'stool_test': 'Fecal analysis and screening results',
        
        # Imaging & Radiology
        'chest_xray_report': 'Chest X-ray imaging report',
        'abdominal_xray_report': 'Abdominal X-ray imaging findings',
        'ct_scan_report': 'CT scan imaging and analysis',
        'mri_scan_report': 'MRI imaging report and findings',
        'ultrasound_report': 'Ultrasound imaging examination',
        'mammography_report': 'Breast mammography examination',
        'bone_density_scan': 'DEXA scan and osteoporosis screening',
        'pet_scan_report': 'PET scan nuclear imaging results',
        'angiography_report': 'Angiogram and vascular imaging',
        'spine_imaging_report': 'Spine X-ray or imaging study',
        'joint_imaging_report': 'Joint X-ray or imaging examination',
        
        # Medications & Pharmacy
        'prescription_receipt': 'Pharmacy prescription documentation',
        'pharmacy_receipt': 'Medication purchase receipt and history',
        'medication_list': 'Current medications and dosages',
        'medication_reconciliation': 'Complete medication review and list',
        'antibiotic_prescription': 'Antibiotic medication prescription',
        'pain_medication_prescription': 'Pain management medication prescription',
        'allergy_medication_prescription': 'Allergy and antihistamine prescription',
        'chronic_disease_medication': 'Long-term chronic disease medications',
        
        # Dental
        'dental_exam_report': 'Dental examination and findings',
        'dental_cleaning_receipt': 'Teeth cleaning and prophylaxis receipt',
        'dental_xray_report': 'Dental radiograph imaging report',
        'root_canal_report': 'Root canal procedure documentation',
        'cavity_filling_receipt': 'Cavity filling procedure documentation',
        'orthodontist_report': 'Braces and orthodontic treatment notes',
        'extraction_report': 'Tooth extraction procedure documentation',
        
        # Eye & Vision
        'eye_exam_report': 'Eye examination and vision assessment',
        'optometrist_prescription': 'Glasses and contact lens prescription',
        'ophthalmologist_report': 'Specialist eye care evaluation',
        'vision_correction_prescription': 'Eye prescription for corrections',
        'glaucoma_screening': 'Intraocular pressure and glaucoma testing',
        
        # Mental Health & Behavioral
        'psychiatry_notes': 'Psychiatrist consultation and treatment notes',
        'therapy_session_notes': 'Mental health counseling session notes',
        'psychoeducational_evaluation': 'Psychological and educational testing',
        'depression_screening': 'Depression assessment screening results',
        'anxiety_assessment': 'Anxiety disorder assessment and evaluation',
        'substance_abuse_evaluation': 'Addiction and substance use assessment',
        
        # Surgical & Procedures
        'surgery_summary': 'Surgical procedure documentation',
        'anesthesia_report': 'Anesthesia and perioperative report',
        'biopsy_results': 'Tissue biopsy analysis and findings',
        'colonoscopy_report': 'Colonoscopy procedure and findings',
        'endoscopy_report': 'Upper endoscopy procedure documentation',
        'echocardiogram_report': 'Heart ultrasound imaging results',
        'stress_test_report': 'Cardiac stress test results',
        'catheterization_report': 'Cardiac catheterization procedure',
        'pacemaker_report': 'Pacemaker implant procedure and settings',
        
        # Immunizations & Vaccines
        'vaccination_record': 'Immunization and vaccination record',
        'immunization_schedule': 'Vaccination schedule and recommendations',
        'covid_vaccination_record': 'COVID-19 vaccination documentation',
        'flu_shot_receipt': 'Influenza vaccination record',
        'travel_vaccination': 'Travel-required vaccination documentation',
        
        # Pregnancy & Obstetrics
        'prenatal_visit_notes': 'Pregnancy visit notes and monitoring',
        'obstetric_ultrasound': 'Pregnancy ultrasound imaging report',
        'labor_delivery_report': 'Delivery and birth documentation',
        'postpartum_summary': 'Postpartum discharge and follow-up',
        'obgyn_consultation': 'Obstetrics/gynecology specialist visit',
        
        # Emergency & Urgent Care
        'emergency_room_report': 'Emergency department visit documentation',
        'urgent_care_note': 'Urgent care clinic visit report',
        'ambulance_report': 'EMS and ambulance transport documentation',
        'trauma_assessment': 'Trauma and injury assessment',
        
        # Hospital & Inpatient
        'hospital_admission_note': 'Hospital admission documentation',
        'hospital_discharge_summary': 'Hospital discharge paperwork',
        'physicians_orders': 'Doctor treatment orders during hospitalization',
        'nursing_notes': 'Nursing care documentation',
        'hospital_bill': 'Hospital charges and billing statement',
        
        # Specialist Consultations
        'cardiology_consultation': 'Heart specialist consultation',
        'dermatology_report': 'Skin specialist examination',
        'orthopedic_report': 'Bone and joint specialist evaluation',
        'neurology_consultation': 'Neurologist specialist consultation',
        'gastroenterology_report': 'Digestive system specialist report',
        
        # Home Health & Rehabilitation
        'home_health_visit_note': 'Home health nurse visit documentation',
        'physical_therapy_evaluation': 'PT assessment and treatment plan',
        'occupational_therapy_note': 'OT evaluation and treatment plan',
        'speech_therapy_note': 'Speech-language pathology treatment',
        'home_care_plan': 'Home care plan and instructions',
        
        # Administrative & Work-Related
        'disability_evaluation': 'Disability determination evaluation',
        'fmla_certification': 'FMLA medical certification form',
        'work_restrictions_form': 'Work duty restrictions documentation',
        'medical_leave_documentation': 'Medical leave authorization',
        'insurance_claim_form': 'Insurance claim submission form',
        'prior_authorization': 'Prior authorization for procedures',
        'medical_records_request': 'Medical records request documentation'
    }
    
    EXTRACTION_PROMPT = """You are a medical data extraction specialist with expertise in parsing diverse clinical documents.

Extract ALL available information from this medical document. Adapt extraction based on document type.

CORE FIELDS (extract if present):
- age: integer (patient's age in years)
- ethnicity: string (patient's ethnicity/race)
- gender: string (patient's gender)
- patient_name: string (patient name if available)
- document_type: classification of document type (see list below)

DOCUMENT TYPE CLASSIFICATION:
Primary Care: annual_physical, general_practitioner_notes, office_visit_note, patient_summary
Lab Results: blood_test_results, urinalysis, cholesterol_panel, glucose_test, complete_blood_count, metabolic_panel, thyroid_function_test, covid_test_result, allergy_test_results, drug_screening_result, pregnancy_test_result, coagulation_test, liver_function_test, kidney_function_test, testosterone_test, stool_test
Imaging: chest_xray_report, abdominal_xray_report, ct_scan_report, mri_scan_report, ultrasound_report, mammography_report, bone_density_scan, pet_scan_report, angiography_report, spine_imaging_report, joint_imaging_report
Medications: prescription_receipt, pharmacy_receipt, medication_list, medication_reconciliation, antibiotic_prescription, pain_medication_prescription, allergy_medication_prescription, chronic_disease_medication
Dental: dental_exam_report, dental_cleaning_receipt, dental_xray_report, root_canal_report, cavity_filling_receipt, orthodontist_report, extraction_report
Eye Care: eye_exam_report, optometrist_prescription, ophthalmologist_report, vision_correction_prescription, glaucoma_screening
Mental Health: psychiatry_notes, therapy_session_notes, psychoeducational_evaluation, depression_screening, anxiety_assessment, substance_abuse_evaluation
Surgical/Procedures: surgery_summary, anesthesia_report, biopsy_results, colonoscopy_report, endoscopy_report, echocardiogram_report, stress_test_report, catheterization_report, pacemaker_report
Immunizations: vaccination_record, immunization_schedule, covid_vaccination_record, flu_shot_receipt, travel_vaccination
Pregnancy/OB: prenatal_visit_notes, obstetric_ultrasound, labor_delivery_report, postpartum_summary, obgyn_consultation
Emergency/Urgent: emergency_room_report, urgent_care_note, ambulance_report, trauma_assessment
Hospital: hospital_admission_note, hospital_discharge_summary, physicians_orders, nursing_notes, hospital_bill
Specialists: cardiology_consultation, dermatology_report, orthopedic_report, neurology_consultation, gastroenterology_report
Home Health: home_health_visit_note, physical_therapy_evaluation, occupational_therapy_note, speech_therapy_note, home_care_plan
Administrative: disability_evaluation, fmla_certification, work_restrictions_form, medical_leave_documentation, insurance_claim_form, prior_authorization, medical_records_request

CONDITIONAL FIELDS (extract based on document type):

FOR LAB REPORTS:
- lab_results: dictionary with test names as keys and values with units
- lab_date: date of lab work
- reference_ranges: normal reference ranges if provided
- abnormal_flags: any values flagged as abnormal or critical

FOR CLINICAL NOTES & OFFICE VISITS:
- visit_date: date of visit
- chief_complaint: reason for visit
- clinical_findings: list of findings
- assessment_plan: treatment plan
- vital_signs: blood pressure, temperature, heart rate, etc.

FOR PRESCRIPTIONS & MEDICATIONS:
- medications: list of {name, dosage, frequency, duration}
- prescriber: name of prescriber
- date_prescribed: date
- pharmacy_info: pharmacy name if available

FOR IMAGING REPORTS:
- imaging_type: type of imaging (X-ray, MRI, CT, etc.)
- findings: list of findings
- impression: overall impression
- exam_date: date of exam
- comparison: comparison to prior studies if mentioned

FOR SURGICAL REPORTS:
- surgery_type: type of surgery
- surgery_date: date of surgery
- surgeon: surgeon name
- findings: surgical findings
- complications: any complications
- anesthesia_type: type of anesthesia used

FOR DENTAL REPORTS:
- dental_findings: tooth numbers and issues identified
- treatment_type: type of dental work performed
- dentist: dentist name
- treatment_date: date of treatment

FOR VACCINATION RECORDS:
- vaccines_administered: list of vaccines given
- vaccination_dates: dates of vaccinations
- next_due: next vaccination due date if applicable

FOR ALL DOCUMENTS:
- conditions: list of strings (diagnosed medical conditions/diagnoses only, not symptoms)
- medications: list of current medications if mentioned
- allergies: list of known allergies
- providers: list of healthcare providers mentioned

CRITICAL RULES:
1. Return ONLY valid JSON, no markdown formatting, no code blocks, no explanations
2. If a field is missing or unclear, use null (not empty string or empty array)
3. For conditions/diagnoses, extract only confirmed diagnoses (not symptoms or ruled-out conditions)
4. For lab_results, include test name, numeric value, and unit
5. Add confidence_score (0.0-1.0) indicating overall extraction certainty
6. Include document_type classification (use one from the list above)
7. Return null for fields that don't apply to this document type

Expected JSON structure:
{
    "age": 45,
    "gender": "Male",
    "ethnicity": "Asian",
    "patient_name": null,
    "document_type": "blood_test_results",
    "conditions": ["Type 2 Diabetes", "Hypertension"],
    "medications": ["Metformin 1000mg daily", "Lisinopril 10mg daily"],
    "allergies": ["Penicillin"],
    "providers": ["Dr. Johnson", "Dr. Smith"],
    "lab_results": {
        "HbA1c": "7.2%",
        "Blood_Pressure": "140/90 mmHg",
        "LDL_Cholesterol": "130 mg/dL"
    },
    "lab_date": "2024-01-15",
    "reference_ranges": {
        "HbA1c": "<5.7%"
    },
    "abnormal_flags": ["HbA1c: HIGH"],
    "confidence_score": 0.95
}

If this is NOT a medical document (e.g., cat photo, random image, non-medical content):
{
    "error": "Not a medical document",
    "document_type": "non_medical",
    "confidence_score": 0.0
}
"""

    @staticmethod
    async def validate_medical_document(file_path: str) -> Dict:
        """
        Pre-screening to detect non-medical uploads
        
        Args:
            file_path: Path to the uploaded file
            
        Returns:
            Dict with validation results
        """
        validation_prompt = """Analyze this document and respond with ONLY a JSON object (no markdown):

{
    "is_medical_document": true or false,
    "document_type": "one of the 80 medical document types listed below, or non_medical",
    "confidence": 0.0 to 1.0,
    "reason": "brief explanation"
}

MEDICAL DOCUMENT TYPES (80 TOTAL):

PRIMARY CARE & GENERAL (6):
- annual_physical: Annual physical exam report and findings
- general_practitioner_notes: GP visit notes and clinical observations
- office_visit_note: Primary care office visit documentation
- patient_summary: Medical summary letter from healthcare provider
- health_insurance_form: Insurance claim and eligibility forms
- referral_letter: Referral to specialist or other provider

LAB & TEST RESULTS (16):
- blood_test_results: General blood test and serology results
- urinalysis: Urine test results and analysis
- cholesterol_panel: Lipid panel and cholesterol levels
- glucose_test: Blood glucose and diabetes screening
- complete_blood_count: CBC results with cell counts
- metabolic_panel: Comprehensive metabolic panel (CMP)
- thyroid_function_test: TSH and thyroid hormone levels
- covid_test_result: COVID-19 PCR or antigen test result
- allergy_test_results: Allergy testing and sensitivity results
- drug_screening_result: Substance screening test results
- pregnancy_test_result: Pregnancy confirmation test results
- coagulation_test: PT/INR and blood clotting studies
- liver_function_test: Liver enzyme and function tests
- kidney_function_test: Renal function and creatinine levels
- testosterone_test: Hormone level testing results
- stool_test: Fecal analysis and screening results

IMAGING & RADIOLOGY (11):
- chest_xray_report: Chest X-ray imaging report
- abdominal_xray_report: Abdominal X-ray imaging findings
- ct_scan_report: CT scan imaging and analysis
- mri_scan_report: MRI imaging report and findings
- ultrasound_report: Ultrasound imaging examination
- mammography_report: Breast mammography examination
- bone_density_scan: DEXA scan and osteoporosis screening
- pet_scan_report: PET scan nuclear imaging results
- angiography_report: Angiogram and vascular imaging
- spine_imaging_report: Spine X-ray or imaging study
- joint_imaging_report: Joint X-ray or imaging examination

MEDICATIONS & PHARMACY (8):
- prescription_receipt: Pharmacy prescription documentation
- pharmacy_receipt: Medication purchase receipt and history
- medication_list: Current medications and dosages
- medication_reconciliation: Complete medication review and list
- antibiotic_prescription: Antibiotic medication prescription
- pain_medication_prescription: Pain management medication prescription
- allergy_medication_prescription: Allergy and antihistamine prescription
- chronic_disease_medication: Long-term chronic disease medications

DENTAL (7):
- dental_exam_report: Dental examination and findings
- dental_cleaning_receipt: Teeth cleaning and prophylaxis receipt
- dental_xray_report: Dental radiograph imaging report
- root_canal_report: Root canal procedure documentation
- cavity_filling_receipt: Cavity filling procedure documentation
- orthodontist_report: Braces and orthodontic treatment notes
- extraction_report: Tooth extraction procedure documentation

EYE & VISION (5):
- eye_exam_report: Eye examination and vision assessment
- optometrist_prescription: Glasses and contact lens prescription
- ophthalmologist_report: Specialist eye care evaluation
- vision_correction_prescription: Eye prescription for corrections
- glaucoma_screening: Intraocular pressure and glaucoma testing

MENTAL HEALTH & BEHAVIORAL (6):
- psychiatry_notes: Psychiatrist consultation and treatment notes
- therapy_session_notes: Mental health counseling session notes
- psychoeducational_evaluation: Psychological and educational testing
- depression_screening: Depression assessment screening results
- anxiety_assessment: Anxiety disorder assessment and evaluation
- substance_abuse_evaluation: Addiction and substance use assessment

SURGICAL & PROCEDURES (9):
- surgery_summary: Surgical procedure documentation
- anesthesia_report: Anesthesia and perioperative report
- biopsy_results: Tissue biopsy analysis and findings
- colonoscopy_report: Colonoscopy procedure and findings
- endoscopy_report: Upper endoscopy procedure documentation
- echocardiogram_report: Heart ultrasound imaging results
- stress_test_report: Cardiac stress test results
- catheterization_report: Cardiac catheterization procedure
- pacemaker_report: Pacemaker implant procedure and settings

IMMUNIZATIONS & VACCINES (5):
- vaccination_record: Immunization and vaccination record
- immunization_schedule: Vaccination schedule and recommendations
- covid_vaccination_record: COVID-19 vaccination documentation
- flu_shot_receipt: Influenza vaccination record
- travel_vaccination: Travel-required vaccination documentation

PREGNANCY & OBSTETRICS (5):
- prenatal_visit_notes: Pregnancy visit notes and monitoring
- obstetric_ultrasound: Pregnancy ultrasound imaging report
- labor_delivery_report: Delivery and birth documentation
- postpartum_summary: Postpartum discharge and follow-up
- obgyn_consultation: Obstetrics/gynecology specialist visit

EMERGENCY & URGENT CARE (4):
- emergency_room_report: Emergency department visit documentation
- urgent_care_note: Urgent care clinic visit report
- ambulance_report: EMS and ambulance transport documentation
- trauma_assessment: Trauma and injury assessment

HOSPITAL & INPATIENT (5):
- hospital_admission_note: Hospital admission documentation
- hospital_discharge_summary: Hospital discharge paperwork
- physicians_orders: Doctor treatment orders during hospitalization
- nursing_notes: Nursing care documentation
- hospital_bill: Hospital charges and billing statement

SPECIALIST CONSULTATIONS (5):
- cardiology_consultation: Heart specialist consultation
- dermatology_report: Skin specialist examination
- orthopedic_report: Bone and joint specialist evaluation
- neurology_consultation: Neurologist specialist consultation
- gastroenterology_report: Digestive system specialist report

HOME HEALTH & REHABILITATION (5):
- home_health_visit_note: Home health nurse visit documentation
- physical_therapy_evaluation: PT assessment and treatment plan
- occupational_therapy_note: OT evaluation and treatment plan
- speech_therapy_note: Speech-language pathology treatment
- home_care_plan: Home care plan and instructions

ADMINISTRATIVE & WORK-RELATED (7):
- disability_evaluation: Disability determination evaluation
- fmla_certification: FMLA medical certification form
- work_restrictions_form: Work duty restrictions documentation
- medical_leave_documentation: Medical leave authorization
- insurance_claim_form: Insurance claim submission form
- prior_authorization: Prior authorization for procedures
- medical_records_request: Medical records request documentation

Non-medical includes: photos, random images, personal letters, unrelated documents, blank pages.
"""
        
        try:
            # Upload file
            with open(file_path, 'rb') as f:
                uploaded_file = genai.upload_file(f, mime_type='application/pdf')
            
            # Generate response
            response = genai.GenerativeModel(MODEL_ID).generate_content(
                [
                    uploaded_file,
                    validation_prompt
                ]
            )
            
            # Clean response text
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            return {
                "is_valid": result.get('is_medical_document', False) and result.get('confidence', 0) > 0.7,
                "document_type": result.get('document_type', 'unknown'),
                "confidence": result.get('confidence', 0.0),
                "reason": result.get('reason', '')
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return {
                "is_valid": False,
                "document_type": "parse_error",
                "confidence": 0.0,
                "reason": "Failed to parse AI response"
            }
        except Exception as e:
            print(f"Validation error: {e}")
            return {
                "is_valid": False,
                "document_type": "error",
                "confidence": 0.0,
                "reason": str(e)
            }

    @staticmethod
    async def extract_patient_data(file_path: str) -> Dict:
        """
        Extract structured patient data from medical PDF
        
        Args:
            file_path: Path to the medical PDF file
            
        Returns:
            Dict with extraction results
        """
        try:
            # Upload file
            with open(file_path, 'rb') as f:
                uploaded_file = genai.upload_file(f, mime_type='application/pdf')
            
            # Generate extraction
            response = genai.GenerativeModel(MODEL_ID).generate_content(
                [
                    uploaded_file,
                    MedicalDataExtractor.EXTRACTION_PROMPT
                ]
            )
            
            # Clean response text
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Check if error in response
            if "error" in result:
                return {
                    "status": "invalid",
                    "data": None,
                    "error": result["error"]
                }
            
            # Validate at least some key medical information is present
            # Different document types may have different required fields
            has_medical_info = any([
                result.get('age'),
                result.get('conditions'),
                result.get('lab_results'),
                result.get('medications'),
                result.get('imaging_type'),
                result.get('visit_date'),
                result.get('surgery_date'),
                result.get('chief_complaint'),
                result.get('findings'),
                result.get('assessment_plan'),
                result.get('allergies'),
                result.get('document_type')
            ])
            
            if not has_medical_info:
                return {
                    "status": "incomplete",
                    "data": result,
                    "error": "No medical information extracted"
                }
            
            return {
                "status": "success",
                "data": result,
                "error": None
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "data": None,
                "error": f"AI returned malformed JSON: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "error": f"Processing failed: {str(e)}"
            }


# For backwards compatibility
extract_patient_data = MedicalDataExtractor.extract_patient_data
validate_medical_document = MedicalDataExtractor.validate_medical_document