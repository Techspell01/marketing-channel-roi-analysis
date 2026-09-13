import numpy as np
from scipy.stats import chi2_contingency

# Data pulled directly from your BigQuery query results
channels = ["Referral", "Direct", "Organic Search", "Display",
            "Paid Search", "Social", "Affiliates", "(Other)"]
sessions = np.array([104701, 142856, 381137, 6259, 25290, 226020, 16372, 120])
transactions = np.array([5543, 2219, 3581, 152, 479, 131, 9, 1])

non_converting = sessions - transactions

# Build the contingency table: rows = channel, columns = [converted, not converted]
contingency_table = np.array([transactions, non_converting]).T

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Cramer's V: effect size for chi-square (0.1=small, 0.3=medium, 0.5=large)
n = contingency_table.sum()
min_dim = min(contingency_table.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))

print("=== Chi-square test: Channel vs Conversion ===")
print(f"Chi2 statistic: {chi2:.2f}")
print(f"p-value: {p_value:.10f}")
print(f"Cramer's V (effect size): {cramers_v:.4f}", end="  ")
if cramers_v < 0.1:
    print("(negligible)")
elif cramers_v < 0.3:
    print("(small)")
elif cramers_v < 0.5:
    print("(medium)")
else:
    print("(large)")

print("\n=== Conversion rate by channel (sorted) ===")
conv_rate = (transactions / sessions * 100).round(3)
for ch, rate, sess, trans in sorted(zip(channels, conv_rate, sessions, transactions),
                                      key=lambda x: -x[1]):
    print(f"{ch:15s}  {rate:6.3f}%   ({trans} transactions / {sess} sessions)")

print("\nConclusion: If p < 0.05 AND Cramer's V is small/medium/large (not negligible),")
print("this is a real, meaningful, actionable finding -- unlike your two earlier datasets.")
