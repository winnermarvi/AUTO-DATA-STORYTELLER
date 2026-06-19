import matplotlib.pyplot as plt

def plot_feature_importance(feature_importance):

    features = [item[0] for item in feature_importance]
    scores = [item[1] for item in feature_importance]

    plt.figure(figsize=(8,5))

    plt.barh(features,scores)

    plt.xlabel("Importance Score")
    plt.ylabel("Features")
    plt.title("Top Feature Importance")

    plt.tight_layout()

    plt.savefig("src/reports/charts/feature_importance.png")

    plt.close()