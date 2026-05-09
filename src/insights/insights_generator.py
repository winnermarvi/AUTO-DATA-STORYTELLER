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
        
        #if mean is 0 we only take std else we use variation formula (std/mean) if variation is above 0.3 its high variation else low variation

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
    for key in report['categorical_summary']:

        if((int(report['categorical_summary'][key]['unique'])/int(rows)) > 0.9 and int(rows)>50):
            insights.append(f"Column {key} appears to contain highly unique identifier-like values")
        else:
            insights.append(f"Column {key} has {report['categorical_summary'][key]['unique']} unique categories")
            top = report['categorical_summary'][key]['top']
            if top is None:
                insights.append(f"In column {key} no dominant category found")
            else:
                insights.append(f"Most common value in {key} is {top}")

    
    return insights