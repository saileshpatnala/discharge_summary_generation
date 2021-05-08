import pandas as pd


def split_dataset():

    # load data set
    data_set = pd.read_csv('./prepared_dataset.csv')
    data_set = data_set.sample(frac=1)

    # split and save train, val and test
    train = data_set.iloc[:23990, 1:]
    train.to_csv('train.csv')

    val = data_set.iloc[23990:29990, 1:]
    val.to_csv('validation.csv')

    test = data_set.iloc[29990:, 1:]
    test.to_csv('test.csv')


if __name__ == '__main__':
    split_dataset()
