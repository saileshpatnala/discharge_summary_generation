import re
from data_preparation_claus.params import Params


class TextCleaner:

    def __init__(self, text_raw, category):
        self.text_raw = text_raw
        self.category = category

    def clean_text(self):
        if self.category == Params.ECHO_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.ECG_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.NURSING_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.PHYSICIAN_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.REHAB_SERVICES_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.CASE_MANAGEMENT_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.RESPIRATORY_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.NUTRITION_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.GENERAL_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.SOCIAL_WORK_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.PHARMACY_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.CONSULT_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.RADIOLOGY_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.NURSING_OTHER_CATEGORY_VALUE_STR:
            pass
        elif self.category == Params.DISCHARGE_SUMMARY_CATEGORY_VALUE_STR:
            # text_temp = re.findall(r'Brief Hospital Course:(.*)Medications on Admission:', self.text_raw)
            start_idx = self.text_raw.find('Brief Hospital Course:')
            if start_idx == -1:
                start_idx = self.text_raw.find('HOSPITAL COURSE:')
                if start_idx == -1:
                    res = -1
                else:
                    end_idx = self.text_raw.find('MEDICATIONS ON DISCHARGE:')
                    text_temp = self.text_raw[start_idx:end_idx]
                    res = 1
            else:
                end_idx = self.text_raw.find('Medications on Admission:')
                text_temp = self.text_raw[start_idx:end_idx]
                res = 1
        else:
            print('Unknown category "' + str(self.category) + '" detected..')
            text_temp = ''

        # text_cleaned = text_temp
        return res, self.text_raw



