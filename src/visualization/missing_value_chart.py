import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_missing_values(missing_values):

    column_names = []
    values = []

    for column_name,value in missing_values.items():

        if value > 0:
            column_names.append(column_name)
            values.append(value)
    
    if len(column_names) == 0:
        
        return None

    plt.figure(figsize=(8,5))

    plt.barh(column_names,values)

    plt.xlabel("Missing values")
    plt.ylabel("Columns")
    plt.title("Missing Values by Column")
    
    plt.tight_layout()

    plt.savefig("src/reports/charts/missing_values.png")

    plt.close()