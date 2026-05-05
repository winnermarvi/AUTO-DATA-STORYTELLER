#Giving dataset info from the report we generated

def generate_insights(report):

    insights = []
    
    #Rows and columns
    rows = report['shape']['rows']
    cols = report['shape']['columns']

    insights.append(f"Dataset contains {rows} rows & {cols} columns")

    #missing values 
    total_missing_value = 0
    max_missing = 0
    max_missing_val_col = ""
    for key in report['missing_values']:
        total_missing_value += int(report['missing_values'][key])
        if report['missing_values'][key] > max_missing:
            max_missing = report['missing_values'][key]
            max_missing_val_col = key

    
    if max_missing == 0:
        insights.append(f"No missing values found in dataset")
    else:
        insights.append(f"Total missing values are {total_missing_value}")
        insights.append(f"Column {max_missing_val_col} has the highest missing values ({max_missing} values)")

    #numeric columns
    for key in report['numerical_summary']:
        
        insights.append(f"Average {key} is {report['numerical_summary'][key]['mean']:.2f}")
        insights.append(f"{key} ranges from {int(report['numerical_summary'][key]['min'])} to {int(report['numerical_summary'][key]['max'])}")
        
        if report['numerical_summary'][key]['mean'] == 0:
            if float(report['numerical_summary'][key]['std']) > 0.3:
                insights.append(f"{key} shows high variation")
            else:
                insights.append(f"{key} shows low variation")
        else:
            if float(report['numerical_summary'][key]['std'])/abs(float(report['numerical_summary'][key]['mean'])) > 0.3:
                insights.append(f"{key} shows high variation")
            else:
                insights.append(f"{key} shows low variation")

    #categoric columns

    
    return insights