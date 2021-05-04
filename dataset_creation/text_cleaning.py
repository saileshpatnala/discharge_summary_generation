import re
from dataset_creation.params import Params


class TextCleaner:

    def __init__(self, text_raw, category):
        self.text_raw = text_raw
        self.category = category

    def clean_text(self):
        if self.category == Params.ECHO_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('Conclusions:')
            if start_idx > 0:
                text_temp = self.text_raw[start_idx+12:]
                text_temp = self.final_clean(text_temp)
            else:
                text_temp = ''

        elif self.category == Params.ECG_CATEGORY_VALUE_STR:
            text_temp = self.final_clean(self.text_raw)

        elif self.category == Params.NURSING_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.PHYSICIAN_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.REHAB_SERVICES_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('Diagnosis:')
            end_idx = self.text_raw.find('Goal')
            if (start_idx > 0) and (end_idx > start_idx):
                text_temp = self.text_raw[start_idx + 10: end_idx]
                text_temp = self.final_clean(text_temp)
            else:
                text_temp = ''

        elif self.category == Params.CASE_MANAGEMENT_CATEGORY_VALUE_STR:
            first_line = self.text_raw.split('\n')[0]
            if first_line.find('Discharge') != -1 and first_line.find('Plan') != -1:
                text_temp = ' '.join(self.text_raw.split('\n')[1:])
                text_temp = self.final_clean(text_temp)
            else:
                if (self.text_raw[:21] == 'Insurance information') or (self.text_raw[:21] == 'Insurance Information'):
                    text_temp = ''
                else:
                    query_str_list = re.findall(r'Narrative / Plan [^:]+:', self.text_raw)
                    if len(query_str_list) > 0:
                        query_str = query_str_list[0]
                        start_idx = self.text_raw.find(query_str)
                        text_temp = self.text_raw[start_idx:]
                        start_idx = text_temp.find(':')
                        text_temp = text_temp[start_idx + 1:]
                        text_temp = self.final_clean(text_temp)
                    else:
                        text_temp = ''

        elif self.category == Params.RESPIRATORY_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.NUTRITION_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('Assessment of Nutritional Status')
            if start_idx > 0:
                text_temp = self.text_raw[start_idx + 32:]
                text_temp = self.final_clean(text_temp)
            else:
                text_temp = ''

        elif self.category == Params.GENERAL_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.SOCIAL_WORK_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('Family Assessment:')
            if start_idx > 0:
                end_idx = self.text_raw.find('Clergy Contact:')
                if end_idx < 0:
                    end_idx = self.text_raw.find('Clergy contact:')
                if end_idx > start_idx:
                    text_temp = self.text_raw[start_idx + 18: end_idx]
                    text_temp = self.final_clean(text_temp)
                else:
                    text_temp = ''
            else:
                text_temp = ''

        elif self.category == Params.PHARMACY_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('ASSESSMENT:')
            if start_idx > 0:
                end_idx = self.text_raw.find('RECOMMENDATION:')
                if end_idx > start_idx:
                    text_temp = self.text_raw[start_idx + 11: end_idx]
                    text_temp = self.final_clean(text_temp)
                else:
                    text_temp = ''
            else:
                text_temp = ''

        elif self.category == Params.CONSULT_CATEGORY_VALUE_STR:
            start_idx_1 = self.text_raw.find('HPI')
            start_idx_2 = self.text_raw.find('History of Presented Illnesses')
            start_idx = None
            if start_idx_1 > 0 and start_idx_2 > 0:
                (start_idx, delay) = (start_idx_1, 4) if start_idx_1 < start_idx_2 else (start_idx_2, 30)
            else:
                if start_idx_1 < 0 and start_idx_2 < 0:
                    text_temp = ''
                else:
                    (start_idx, delay) = (start_idx_1, 4) if start_idx_1 > start_idx_2 else (start_idx_2, 30)

            end_idx = None
            if start_idx:
                end_idx_1 = self.text_raw.find('Allergies')
                end_idx_2 = self.text_raw.find('Patient admitted from')
                if end_idx_1 > 0 and end_idx_2 > 0:
                    end_idx = end_idx_1 if end_idx_1 < end_idx_2 else end_idx_2
                else:
                    if end_idx_1 < 0 and end_idx_2 < 0:
                        text_temp = ''
                    else:
                        end_idx = end_idx_1 if end_idx_1 > end_idx_2 else end_idx_2

            if end_idx:
                text_temp = self.text_raw[start_idx + delay: end_idx]
                text_temp = self.final_clean(text_temp)

        elif self.category == Params.RADIOLOGY_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('IMPRESSION:')
            if start_idx > 0:
                text_temp = self.text_raw[start_idx + 11:]
                text_temp = self.final_clean(text_temp)
            else:
                text_temp = ''

        elif self.category == Params.NURSING_OTHER_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.DISCHARGE_SUMMARY_CATEGORY_VALUE_STR:
            start_idx = self.text_raw.find('Brief Hospital Course:')
            if start_idx == -1:
                start_idx = self.text_raw.find('HOSPITAL COURSE:')
                if start_idx == -1:
                    text_temp = ''
                else:
                    end_idx = self.text_raw.find('MEDICATIONS ON DISCHARGE:')
                    text_temp = self.text_raw[start_idx + 16: end_idx]
                    text_temp = self.final_clean(text_temp)
            else:
                end_idx = self.text_raw.find('Medications on Admission:')
                text_temp = self.text_raw[start_idx + 22: end_idx]
                text_temp = self.final_clean(text_temp)

        else:
            print('Unknown category "' + str(self.category) + '" detected..')
            text_temp = ''

        text_cleaned = text_temp

        return text_cleaned

    @classmethod
    def final_clean(cls, text_in):
        text_out = cls.remove_markups(text_in)
        text_out = cls.remove_stars(text_out)
        text_out = cls.to_lower(text_out)
        text_out = cls.clean_underscores(text_out)
        text_out = cls.clear_spaces(text_out)
        return text_out

    @staticmethod
    def remove_markups(text_in):
        text_out = text_in.replace('\n', ' ')
        return text_out

    @staticmethod
    def remove_stars(text_in):
        # text_out = re.sub(r'\[\*\*[^\]|\[]*\*\*]', '', text_in)
        text_out = re.sub(r'\[\*\*[A-Za-z\s]*[Nn]ame[^\]|\[]*\*\*]', '<NAME>', text_in)
        text_out = re.sub(r'\[\*\*[0-9][^\]|\[]*\*\*]', '<DATE>', text_out)
        text_out = re.sub(r'\[\*\*[^\]|\[]*\*\*]', '<ENTITY>', text_out)
        return text_out

    @staticmethod
    def to_lower(text_in):
        text_out = text_in.lower()
        return text_out

    @staticmethod
    def clean_underscores(text_in):
        text_out = text_in.replace('_', '')
        return text_out

    @staticmethod
    def clear_spaces(text_in):
        text_out = re.sub(r' +', ' ', text_in)
        return text_out



