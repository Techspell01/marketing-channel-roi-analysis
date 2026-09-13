"""
Step 2 (v2 dataset): Compare channels/campaign types on ROI, Conversion_Rate, CTR.
Includes effect size (eta-squared) alongside p-values, since with 200k rows
p-values alone can be misleading (almost anything becomes "significant").
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("marketing_campaigns_v2_clean.csv")


def eta_squared(groups):
    """Effect size for ANOVA: how much of the variance is actually explained
    by group membership. Rule of thumb: 0.01 = small, 0.06 = medium, 0.14 = large."""
    all_vals = pd.concat(groups)
    grand_mean = all_vals.mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = sum((all_vals - grand_mean) ** 2)
    return ss_between / ss_total


def compare(df, group_col, value_col):
    print(f"\n=== {value_col} by {group_col} ===")
    summary = df.groupby(group_col)[value_col].agg(["mean", "std", "count"]).round(4)
    summary = summary.sort_values("mean", ascending=False)
    print(summary)

    groups = [df[df[group_col] == g][value_col] for g in df[group_col].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    eta_sq = eta_squared(groups)

    print(f"ANOVA: F={f_stat:.3f}, p={p_value:.6f}")
    print(f"Effect size (eta-squared): {eta_sq:.5f}", end="  ")
    if eta_sq < 0.01:
        print("(negligible — differences are real but practically meaningless)")
    elif eta_sq < 0.06:
        print("(small)")
    elif eta_sq < 0.14:
        print("(medium)")
    else:
        print("(large — this matters)")

    return summary


# ---- Compare Channel_Used ----
channel_roi = compare(df, "Channel_Used", "ROI")
compare(df, "Channel_Used", "Conversion_Rate")
compare(df, "Channel_Used", "CTR")

# ---- Compare Campaign_Type ----
compare(df, "Campaign_Type", "ROI")
compare(df, "Campaign_Type", "Conversion_Rate")

# ---- Compare Customer_Segment ----
compare(df, "Customer_Segment", "ROI")
compare(df, "Customer_Segment", "Conversion_Rate")

# ---- Chart: ROI by Channel_Used ----
plt.figure(figsize=(9, 5))
channel_roi["mean"].plot(kind="bar", color="darkorange")
plt.title("Average ROI by Channel Used")
plt.ylabel("ROI")
plt.xlabel("Channel")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("roi_by_channel_v2.png", dpi=150)
print("\nSaved chart: roi_by_channel_v2.png")

print("\nDone. Look for LOW p-values AND eta-squared > 0.01 together — that's where a real, meaningful pattern is.")
