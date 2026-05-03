

#Handles missing values
def missing_handler(df):
    
    cols_to_drop = []
    threshold = 70


    #Dropping the columns with high missing values
    for i in df.columns:

        missing_percentage = ( df[i].isnull().sum() / df.shape[0] ) * 100 

        if missing_percentage > threshold:
            cols_to_drop.append(i)

    df = df.drop(columns = cols_to_drop)

    #separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns.to_list()
    categoric_cols = df.select_dtypes(exclude=['number']).columns.to_list()

    #filling the missing values
    for i in numeric_cols:
        df[i] = df[i].fillna(df[i].median())

    for i in categoric_cols:
        
        missing_percentage = ( df[i].isnull().sum() / df.shape[0] ) * 100

        if missing_percentage > 30:
            df[i] = df[i].fillna('Unknown')
        else:
            mode_val = df[i].mode()
            top = mode_val.iloc[0] if not mode_val.empty else "Unknown"
            df[i] = df[i].fillna(top)

        

    return df