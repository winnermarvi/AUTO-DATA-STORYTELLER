def validate_intent(intent, df):

    operation = intent["operation"]
    target_column = intent["target_column"]
    group_by = intent["group_by"]

    # Supported operations
    supported_operations = [
        "mean",
        "sum",
        "count",
        "max",
        "min"
    ]

    if operation not in supported_operations:
        return {
            "valid": False,
            "message": f"Unsupported operation: {operation}"
        }

    # Target column must exist
    if target_column is None:
        return {
            "valid": False,
            "message": "I couldn't find the requested column in the dataset."
        }

    if target_column not in df.columns:
        return {
            "valid": False,
            "message": f"Column '{target_column}' does not exist."
        }

    # Group-by column must exist (if provided)
    if group_by is not None:

        if group_by not in df.columns:
            return {
                "valid": False,
                "message": f"Group-by column '{group_by}' does not exist."
            }

    # Numeric operations require numeric columns
    numeric_operations = [
        "mean",
        "sum",
        "max",
        "min"
    ]

    if operation in numeric_operations:

        if not df[target_column].dtype.kind in "biufc":
            return {
                "valid": False,
                "message": f"'{target_column}' is not a numeric column."
            }

    return {
        "valid": True,
        "message": None
    }