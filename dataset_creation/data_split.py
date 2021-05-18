import pandas as pd


def split_dataset():

    # load data set
    data_set = pd.read_csv('mimic-iii_discharge_summary.csv')
    data_set = data_set.sample(frac=1)

    # split and save train, val and test
    train = data_set.iloc[:23990, 1:]
    train.to_csv('train.csv')

    val = data_set.iloc[23990:29990, 1:]
    val.to_csv('validation.csv')

    test = data_set.iloc[29990:, 1:]
    test.to_csv('test.csv')

    # split and save small train, val and test
    train_small = data_set.iloc[:350, 1:]
    train_small.to_csv('train_small.csv')

    val_small = data_set.iloc[350:400, 1:]
    val_small.to_csv('val_small.csv')

    test_small = data_set.iloc[400:500, 1:]
    test_small.to_csv('test_small.csv')


if __name__ == '__main__':
    split_dataset()
