import re
from data_preparation_claus.params import Params


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
            end_idx = self.text_raw.find('Goal') # couldn't figure out how to match \n...
            if (start_idx > 0) and (end_idx > start_idx):
                text_temp = self.text_raw[start_idx + 10: end_idx]
                text_temp = self.final_clean(text_temp)
            else:
                text_temp = ''

        elif self.category == Params.CASE_MANAGEMENT_CATEGORY_VALUE_STR:
            #############missing the discharge plan thing#############
            ############# wasn't sure what exactly we said here we would be doing...##########
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
            pass

        elif self.category == Params.PHARMACY_CATEGORY_VALUE_STR:
            pass

        elif self.category == Params.CONSULT_CATEGORY_VALUE_STR:
            pass

        elif self.category == Params.RADIOLOGY_CATEGORY_VALUE_STR:
            pass

        elif self.category == Params.NURSING_OTHER_CATEGORY_VALUE_STR:
            text_temp = ''

        elif self.category == Params.DISCHARGE_SUMMARY_CATEGORY_VALUE_STR:
            pass

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
        text_out = cls.clear_spaces(text_out)
        return text_out

    @staticmethod
    def remove_markups(text_in):
        text_out = text_in.replace('\n', ' ')
        return text_out

    @staticmethod
    def remove_stars(text_in):
        text_out = re.sub(r'\[\*\*[^\]|\[]*\*\*]', '', text_in)
        return text_out

    @staticmethod
    def to_lower(text_in):
        text_out = text_in.lower()
        return text_out

    @staticmethod
    def clear_spaces(text_in):
        text_out = re.sub(r' +', ' ', text_in)
        return text_out

