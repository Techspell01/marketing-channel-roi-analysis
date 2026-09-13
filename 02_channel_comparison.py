import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("marketing_campaigns_clean.csv")
channel_summary = df.groupby("Marketing_Channel").agg(
    Total_Spend=("Total_Spend", "sum"),
    Total_Revenue=("Revenue_Generated", "sum"),
    Avg_ROI=("ROI", "mean"),
    Avg_CTR=("CTR", "mean"),
    Avg_Conversion_Rate=("Conversion_Rate", "mean"),
    Avg_CPA=("CPA", "mean"),
    Campaign_Count=("Campaign_ID", "count"),
).round(3)

channel_summary["Overall_ROI"] = (
    (channel_summary["Total_Revenue"] - channel_summary["Total_Spend"])
    / channel_summary["Total_Spend"]
).round(3)

channel_summary = channel_summary.sort_values("Overall_ROI", ascending=False)

print("=== Channel Performance Summary ===")
print(channel_summary)
channel_summary.to_csv("channel_summary.csv")

plt.figure(figsize=(8, 5))
channel_summary["Overall_ROI"].plot(kind="bar", color="steelblue")
plt.title("Overall ROI by Marketing Channel")
plt.ylabel("ROI (Revenue - Spend) / Spend")
plt.xlabel("Channel")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("roi_by_channel.png", dpi=150)
print("\nSaved chart: roi_by_channel.png")

best_channel = channel_summary.index[0]
worst_channel = channel_summary.index[-1]

print(f"\n=== Best channel: {best_channel} — breakdown by Age Group ===")
best_by_age = df[df["Marketing_Channel"] == best_channel].groupby("Age_Group")["ROI"].mean().round(3)
print(best_by_age.sort_values(ascending=False))

print(f"\n=== Worst channel: {worst_channel} — breakdown by Age Group ===")
worst_by_age = df[df["Marketing_Channel"] == worst_channel].groupby("Age_Group")["ROI"].mean().round(3)
print(worst_by_age.sort_values(ascending=False))

print("\n=== Spend vs ROI correlation per channel ===")
for channel in df["Marketing_Channel"].unique():
    subset = df[df["Marketing_Channel"] == channel]
    corr = subset["Total_Spend"].corr(subset["ROI"])
    print(f"{channel}: correlation = {corr:.3f}  "
          f"({'diminishing returns' if corr < -0.1 else 'no strong pattern' if abs(corr) <= 0.1 else 'returns increase with spend'})")

print("\nDone. Check roi_by_channel.png and channel_summary.csv for your findings.")
