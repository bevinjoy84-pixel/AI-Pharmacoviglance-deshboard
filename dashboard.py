import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/synthetic_drug_data.csv")

# Drug vs Seriousness
drug_seriousness = pd.crosstab(df["DrugName"], df["Seriousness"])

print(drug_seriousness)

# Select Top 10 Drugs
top10 = df["DrugName"].value_counts().head(10).index
drug_seriousness = drug_seriousness.loc[top10]

# Plot
drug_seriousness.plot(
    kind="bar",
    stacked=True,
    figsize=(10,6)
)

plt.title("Top 10 Drugs vs Seriousness")
plt.xlabel("Drug Name")
plt.ylabel("Number of ADR Reports")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()