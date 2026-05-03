#Handles outliers
def handle_outliers(df):
    
    numerical_cols = df.select_dtypes(include = ['number']).columns.to_list()

    for i in numerical_cols:
        
        Q1 = df[i].quantile(0.25)
        Q3 = df[i].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        df[i] = df[i].clip( lower = lower_bound, upper = upper_bound)



    return df