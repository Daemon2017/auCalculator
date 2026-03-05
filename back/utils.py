from io import StringIO

import pandas as pd


def get_names_data_df(data):
    data_io = StringIO(data)
    data_df = pd.read_csv(data_io, sep=",", header=None)
    names_df = pd.DataFrame(data_df[0])
    data_df = data_df.drop([0], axis=1)
    return names_df, data_df


def apply_prefix(df, prefix):
    if prefix:
        df[0] = prefix + df[0].astype(str)
    return df
