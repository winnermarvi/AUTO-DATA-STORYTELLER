import os

print("Feature Importance:",
      os.path.exists("reports/charts/feature_importance.png"))

print("Missing Values:",
      os.path.exists("reports/charts/missing_values.png"))