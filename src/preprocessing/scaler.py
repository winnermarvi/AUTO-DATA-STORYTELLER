
#scaling huge value for model to understand properly
def scaling(df):

    numeric_cols = df.select_dtypes(include = ['float64','int64']).columns.to_list()

    for i in numeric_cols:

        if df[i].nunique() <= 2:
            continue

        mean = df[i].mean()
        std = df[i].std()

        if std != 0:
            df[i] = (df[i] - mean) / std

    return df