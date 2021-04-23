import re
import tqdm
import pandas as pd

from datetime import datetime
from string import punctuation
from data_preparation_claus.params import Params


class DataPreparer:

    @classmethod
    def create_data_set(cls):
        print('Started data set creation process...')

        data_dict = cls.create_data_dict()

        dataset = []
        print('Creating final data set...')
        for hadm_id, category_dict in data_dict.items():

            # get output
            y = category_dict.get(Params.DISCHARGE_SUMMARY_CATEGORY_VALUE_STR)

            # check it data point is relevant and has a discharge summary
            if not y:
                continue

            else:
                # get input
                x = ''
                entries = []
                for category in Params.OTHER_VALUES_CATEGORY_STR_LIST:
                    for entry in data_dict.get(hadm_id).get(category):
                        entries.append(entry)
                entries_sorted = sorted(entries, key=lambda x: x[1])
                for entry in entries_sorted:
                    x += entry[0]
                    x += ' '
                if len(x) > 1000:
                    dataset.append([str(hadm_id), x, y[0]])

        # save data set
        print('Saving final data set...')
        df = pd.DataFrame(dataset, columns=['HADM_ID', 'Input Text', 'Output Text'])
        df.to_csv('prepared_dataset.csv')

        print('Finished data set creation.')

    @classmethod
    def create_data_dict(cls):
        print('--Started data dict creation process...')

        # get data as pandas dataframe
        data = cls.load_data()

        # create list for first level dictionary with all HADM IDs and a category dictionary as a value
        unique_hadm_id_list = data[Params.HADM_ID_STR].dropna().unique()

        # create list for second level dictionary with all different categories
        unique_categories_list = data[Params.CATEGORY_STR].dropna().unique()

        # dictionary
        data_dict = {hadm_id: {category: [] for category in unique_categories_list} for hadm_id in unique_hadm_id_list}

        # fill dictionary
        print('--Creating data dict...')
        for hadm_id in tqdm.tqdm(unique_hadm_id_list):

            # get relevant rows for current HADM_ID
            relevant_rows = data.loc[data[Params.HADM_ID_STR] == hadm_id]

            # extract relevant categories
            for _, row in relevant_rows.iterrows():
                current_category = row[Params.CATEGORY_STR]
                current_store_time = row[Params.STORETIME_STR]
                if not isinstance(current_store_time, str):
                    current_store_time = datetime.strptime('1111-11-11 11:11:11', '%Y-%m-%d %H:%M:%S')
                else:
                    current_store_time = datetime.strptime(current_store_time, '%Y-%m-%d %H:%M:%S')
                current_text_raw = row[Params.TEXT_STR]
                current_text_cleaned = cls.clean_string(current_text_raw)
                data_dict.get(hadm_id).get(current_category).append((str(current_text_cleaned), current_store_time))
        print('--Data dict created.')

        return data_dict

    @classmethod
    def clean_string(cls, string_raw):

        # mark ups
        string_temp = string_raw.replace('\n', ' ')

        # get rid of underscores
        string_temp = string_temp.replace('_', '')

        # get rid of [** ... **] things
        string_temp = re.sub(r'\[\*\*[^\]|\[]*\*\*]', '', string_temp)

        # remove everything that has a number
        string_temp = ' '.join(s for s in string_temp.split() if not any(c.isdigit() for c in s))

        # remove everything that has a special character, except from {.}
        punctuation_set = punctuation.replace('.', '')
        string_temp = ' '.join(s for s in string_temp.split() if not any(c in punctuation_set for c in s))

        # remove any word that contains more than five capital letters
        string_temp = ' '.join(s for s in string_temp.split() if sum(1 for c in s if c.isupper()) < 15)

        # only one white space
        string_temp = re.sub(r' +', ' ', string_temp)

        # final cleaned string
        string_cleaned = string_temp

        return string_cleaned

    @classmethod
    def load_data(cls):
        print('----Started data loading process...')
        data = pd.read_csv(Params.DATA_PATH)
        print('----Data loaded.')

        return data


if __name__ == '__main__':
    DataPreparer.create_data_set()
