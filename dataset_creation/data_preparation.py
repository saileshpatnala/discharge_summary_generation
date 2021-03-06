import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from dataset_creation.params import Params
from dataset_creation.text_cleaning import TextCleaner


class DataPreparer:

    @classmethod
    def create_data_set(cls):
        print('Started data set creation process...')

        data_dict = cls.create_data_dict()

        dataset = []
        print('Creating final data set...')
        input_text_len_list = []
        output_text_len_list = []
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
                if len(x) > 1000 and len(y[0][0]) > 100:
                    input_text_len_list.append(len(x.split()))
                    output_text_len_list.append(len(y[0][0].split()))
                    dataset.append([str(hadm_id), x, y[0][0]])

        # text length statistics
        print('Input Text Length:')
        print('---- Max:', np.max(input_text_len_list))
        print('---- Average:', np.mean(input_text_len_list))
        print('---- Min:', np.min(input_text_len_list))
        print('Output Text Length:')
        print('---- Max:', np.max(output_text_len_list))
        print('---- Average:', np.mean(output_text_len_list))
        print('---- Min:', np.min(output_text_len_list))

        # plot distribution
        plt.hist(x=input_text_len_list, bins=100)
        plt.xlabel('Bins')
        plt.ylabel('#Strings in bin')
        plt.title('Distribution of Input Text Length')
        plt.savefig('./input_test_length_distribution.png', dpi=400)
        plt.close()

        plt.hist(x=output_text_len_list, bins=100)
        plt.xlabel('Bins')
        plt.ylabel('#Strings in bin')
        plt.title('Distribution of Output Text Length')
        plt.savefig('./output_text_length_distribution.png', dpi=400)
        plt.close()

        # save data set
        print('Saving final data set...')
        df = pd.DataFrame(dataset, columns=['hadm_id', 'input_text', 'output_text'])
        df.to_csv('mimic-iii_discharge_summary.csv')

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
                current_text_cleaned = TextCleaner(text_raw=current_text_raw, category=current_category).clean_text()
                data_dict.get(hadm_id).get(current_category).append((str(current_text_cleaned), current_store_time))
        print('--Data dict created.')

        return data_dict

    @classmethod
    def load_data(cls):
        print('----Started data loading process...')
        data = pd.read_csv(Params.DATA_PATH)
        print('----Data loaded.')

        return data


if __name__ == '__main__':
    DataPreparer.create_data_set()
