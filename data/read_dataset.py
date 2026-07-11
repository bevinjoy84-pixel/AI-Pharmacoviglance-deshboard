import pandas as pd

df = pd.read_csv("data/synthetic_drug_data.csv")

print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)