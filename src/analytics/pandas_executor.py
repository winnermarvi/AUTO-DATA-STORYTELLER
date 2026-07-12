def execute_query(df, intent):

    operation = intent["operation"]
    target_column = intent["target_column"]
    group_by = intent["group_by"]


    # No Group By
    if group_by is None:

        if operation == "mean":
            return df[target_column].mean()

        elif operation == "sum":
            return df[target_column].sum()

        elif operation == "count":
            return df[target_column].count()

        elif operation == "max":
            return df[target_column].max()

        elif operation == "min":
            return df[target_column].min()

        else:
            raise ValueError(f"Unsupported operation: {operation}")

  
    # Group By
    else:

        if operation == "mean":
            return df.groupby(group_by)[target_column].mean()

        elif operation == "sum":
            return df.groupby(group_by)[target_column].sum()

        elif operation == "count":
            return df.groupby(group_by)[target_column].count()

        elif operation == "max":
            return df.groupby(group_by)[target_column].max()

        elif operation == "min":
            return df.groupby(group_by)[target_column].min()

        else:
            raise ValueError(f"Unsupported operation: {operation}")