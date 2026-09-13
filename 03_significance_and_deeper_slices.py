"""
Step 5: Test whether channel differences are statistically significant,
then dig into other slices (Campaign_Name, Location, Age x Channel) for real signal.
"""

import pandas as pd
from scipy import stats

df = pd.read_csv("marketing_campaigns_clean.csv")

# ---- 1. ANOVA: is there a significant ROI difference across channels? ----
channels = df["Marketing_Channel"].unique()
groups = [df[df["Marketing_Channel"] == c]["ROI"] for c in channels]

f_stat, p_value = stats.f_oneway(*groups)
print("=== One-way ANOVA: ROI across Marketing Channels ===")
print(f"F-statistic: {f_stat:.3f}")
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("=> Statistically significant difference exists between channels.")
else:
    print("=> No statistically significant difference between channels (p >= 0.05).")

# ---- 2. Campaign_Name performance (regardless of channel) ----
print("\n=== ROI by Campaign Name (across all channels) ===")
campaign_summary = df.groupby("Campaign_Name").agg(
    Avg_ROI=("ROI", "mean"),
    Total_Spend=("Total_Spend", "sum"),
    Total_Revenue=("Revenue_Generated", "sum"),
    Count=("Campaign_ID", "count"),
).round(3).sort_values("Avg_ROI", ascending=False)
print(campaign_summary)

campaign_groups = [df[df["Campaign_Name"] == c]["ROI"] for c in df["Campaign_Name"].unique()]
f_stat2, p_value2 = stats.f_oneway(*campaign_groups)
print(f"\nANOVA across Campaign Names: F={f_stat2:.3f}, p={p_value2:.4f}")
print("=> Significant" if p_value2 < 0.05 else "=> Not significant")

# ---- 3. Location performance ----
print("\n=== ROI by Location ===")
location_summary = df.groupby("Location").agg(
    Avg_ROI=("ROI", "mean"),
    Total_Spend=("Total_Spend", "sum"),
    Count=("Campaign_ID", "count"),
).round(3).sort_values("Avg_ROI", ascending=False)
print(location_summary)

location_groups = [df[df["Location"] == l]["ROI"] for l in df["Location"].unique()]
f_stat3, p_value3 = stats.f_oneway(*location_groups)
print(f"\nANOVA across Locations: F={f_stat3:.3f}, p={p_value3:.4f}")
print("=> Significant" if p_value3 < 0.05 else "=> Not significant")

# ---- 4. Channel x Age_Group interaction ----
print("\n=== ROI by Channel x Age_Group (pivot table) ===")
pivot = df.pivot_table(values="ROI", index="Marketing_Channel", columns="Age_Group", aggfunc="mean").round(3)
print(pivot)

# ---- 5. Gender split, just in case ----
print("\n=== ROI by Gender ===")
gender_summary = df.groupby("Gender")["ROI"].mean().round(3)
print(gender_summary)
gender_groups = [df[df["Gender"] == g]["ROI"] for g in df["Gender"].unique()]
if len(gender_groups) == 2:
    t_stat, p_val_gender = stats.ttest_ind(*gender_groups)
    print(f"T-test Gender: t={t_stat:.3f}, p={p_val_gender:.4f}")
    print("=> Significant" if p_val_gender < 0.05 else "=> Not significant")

print("\nDone. Look for the LOWEST p-values above (p < 0.05) — that's where your real signal is, if any.")
