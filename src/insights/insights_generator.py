#Giving dataset info from the report we generated

def generate_insights(report):

    overview_insights = []
    data_quality_insights = []
    numerical_insights = []
    categorical_insights = []
    relation_insights= []
    
    #Rows and columns
    rows = report['shape']['rows']
    cols = report['shape']['columns']

    overview_insights.append(f"Dataset contains {rows} rows & {cols} columns")

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
        data_quality_insights.append(f"No missing values found in dataset")
    else:
        data_quality_insights.append(f"Total missing values are {total_missing_value}")
        data_quality_insights.append(f"Column {max_missing_val_col} has the highest missing values ({max_missing} values)")

    #numeric columns
    for key in report['numerical_summary']:
        
        numerical_insights.append(f"Average {key} is {report['numerical_summary'][key]['mean']:.2f}")
        numerical_insights.append(f"{key} ranges from {int(report['numerical_summary'][key]['min'])} to {int(report['numerical_summary'][key]['max'])}")
        
        #if mean is 0 we only take std else we use variation formula (std/mean) if variation is above 0.3 its high variation else low variation

        if report['numerical_summary'][key]['mean'] == 0:
            if float(report['numerical_summary'][key]['std']) > 0.3:
                numerical_insights.append(f"{key} shows high variation")
            else:
                numerical_insights.append(f"{key} shows low variation")
        else:
            if float(report['numerical_summary'][key]['std'])/abs(float(report['numerical_summary'][key]['mean'])) > 0.3:
                numerical_insights.append(f"{key} shows high variation")
            else:
                numerical_insights.append(f"{key} shows low variation")

    #categoric columns
    for key in report['categorical_summary']:

        if((int(report['categorical_summary'][key]['unique'])/int(rows)) > 0.9 and int(rows)>50):
            categorical_insights.append(f"Column {key} appears to contain highly unique identifier-like values")
        else:
            categorical_insights.append(f"Column {key} has {report['categorical_summary'][key]['unique']} unique categories")
            top = report['categorical_summary'][key]['top']
            if top is None:
                categorical_insights.append(f"In column {key} no dominant category found")
            else:
                categorical_insights.append(f"Most common value in {key} is {top}")

                # Dominated values check in columns
                dominance_perc = (int(report['categorical_summary'][key]['top_count'])/int(rows) ) * 100

                if dominance_perc < 60:
                    categorical_insights.append(f"Column {key} appears balanced")
                elif dominance_perc >= 60 and dominance_perc <= 80:
                    categorical_insights.append(f"Column {key} is moderately dominated")
                elif dominance_perc > 80 :
                    categorical_insights.append(f"Column {key} is highly dominated")

    
    # Correlation between data set to find relation between columns
    corr_cols = list(report['correlation'].keys())
    
    for i in range(len(corr_cols)):

        for j in range(i+1,len(corr_cols)):

            col1 = corr_cols[i]
            col2 = corr_cols[j]

            corr_val = report['correlation'][col1][col2]

            if corr_val > 0.70 :
                relation_insights.append(f"{col1} and {col2} shows strong positive relation")

            elif corr_val < (-0.70) :
                relation_insights.append(f"{col1} and {col2} shows strong negative relation")
            


    return {"overview" : overview_insights,
            "data_quality" : data_quality_insights,
            "numerical" : numerical_insights,
            "categorical" : categorical_insights,
            "relationship" : relation_insights
            }