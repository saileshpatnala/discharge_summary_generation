

class Params:

    DATA_PATH = '../data/mimic-iii-clinical-database-1.4/mimic-iii-clinical-database-1.4/NOTEEVENTS.csv'
    # DATA_PATH = './Archive/random_subset.csv'

    # Table attributes
    HADM_ID_STR = 'HADM_ID'
    CATEGORY_STR = 'CATEGORY'
    DESCRIPTION_STR = 'DESCRIPTION'
    TEXT_STR = 'TEXT'
    STORETIME_STR = 'STORETIME'

    # Category attribute - table values
    DISCHARGE_SUMMARY_CATEGORY_VALUE_STR = 'Discharge summary'
    ECHO_CATEGORY_VALUE_STR = 'Echo'
    ECG_CATEGORY_VALUE_STR = 'ECG'
    NURSING_CATEGORY_VALUE_STR = 'Nursing'
    PHYSICIAN_CATEGORY_VALUE_STR = 'Physician '
    REHAB_SERVICES_CATEGORY_VALUE_STR = 'Rehab Services'
    CASE_MANAGEMENT_CATEGORY_VALUE_STR = 'Case Management '
    RESPIRATORY_CATEGORY_VALUE_STR = 'Respiratory '
    NUTRITION_CATEGORY_VALUE_STR = 'Nutrition'
    GENERAL_CATEGORY_VALUE_STR = 'General'
    SOCIAL_WORK_CATEGORY_VALUE_STR = 'Social Work'
    PHARMACY_CATEGORY_VALUE_STR = 'Pharmacy'
    CONSULT_CATEGORY_VALUE_STR = 'Consult'
    RADIOLOGY_CATEGORY_VALUE_STR = 'Radiology'
    NURSING_OTHER_CATEGORY_VALUE_STR = 'Nursing/other'
    OTHER_VALUES_CATEGORY_STR_LIST = ['Echo', 'ECG', 'Nursing', 'Physician ', 'Rehab Services',
                                      'Case Management ', 'Respiratory ', 'Nutrition', 'General', 'Social Work',
                                      'Pharmacy', 'Consult', 'Radiology', 'Nursing/other']

