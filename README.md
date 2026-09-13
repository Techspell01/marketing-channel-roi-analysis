# Marketing Channel ROI Analysis

**Business question:** Which marketing channel actually drives the most value — and is
that difference real, or just noise?

## Summary

This project analyzes marketing channel performance across three datasets, using
proper statistical validation (not just eyeballing charts) at every stage. Two
practice datasets turned out to have no real signal — a legitimate and important
finding in itself. The third, built from real e-commerce session data, revealed a
genuine, statistically significant, and highly actionable pattern.

**Headline finding:** Referral traffic converts at **5.29%** — roughly **9x better**
than Organic Search (0.94%) and **~100x better** than Social (0.058%) or Affiliates
(0.055%) — despite Organic Search having over 3x more sessions. Referral also
generates the highest total revenue ($717,600) of any channel, even though it's far
from the highest-traffic one. Confirmed with a chi-square test (p < 0.00001).

## Method

### Phase 1-2: Synthetic practice datasets (Python / pandas)
- Cleaned and calculated KPIs (ROI, CTR, conversion rate, CPA) on two Kaggle/HF
  marketing datasets (2,000 and 200,000 rows).
- Ran ANOVA tests plus effect size (eta-squared) on channel, campaign type, location,
  customer segment, and gender.
- **Result: no statistically significant or practically meaningful differences found
  in either dataset** — both were confirmed to be randomly generated, not real
  business data. This is documented rather than hidden, since correctly identifying
  noise (instead of manufacturing a false insight) is itself the point.

### Phase 3: Real data (SQL / Google BigQuery)
- Queried the public `google_analytics_sample` dataset (real, obfuscated GA360
  session data from the Google Merchandise Store, ~1M+ sessions over one year).
- Aggregated sessions, transactions, revenue, and conversion rate by channel.
- See `bigquery_queries.sql` for the exact queries.

### Phase 4: Statistical validation (Python / scipy)
- Ran a chi-square test of independence (channel vs. conversion) since conversion
  rate is a proportion, not a continuous metric — the right test for this kind of
  question.
- Result: **p < 0.00001**, Cramer's V = 0.133 — a real, non-random effect, and (per
  the raw conversion-rate gaps) one large enough to be practically significant even
  though its formal effect-size label is "small."

### Phase 5: Dashboard (Power BI)
- Built an interactive dashboard from the BigQuery results: conversion rate by
  channel, total revenue by channel, and total revenue summary card.

## Files

- `01_clean_and_kpis.py`, `02_channel_comparison.py`, `03_significance_and_deeper_slices.py`
  — Phase 1 (first synthetic dataset)
- `01b_clean_v2.py`, `02b_channel_comparison_v2.py` — Phase 2 (second synthetic dataset)
- `bigquery_queries.sql` — Phase 3 (real data queries)
- `04_chisquare_real_data.py` — Phase 4 (significance test on real data)
- `dashboard_screenshot.png` — Phase 5 (Power BI dashboard)

## Tools used

Python (pandas, scipy, matplotlib), SQL (Google BigQuery), Power BI

## Key takeaway

A large sample size or a nice-looking bar chart doesn't mean a finding is real.
Two of the three datasets analyzed here showed *some* visible spread between
channels — but only one of them held up under a proper significance and effect-size
test. That discipline is what separates a reliable business recommendation from a
false positive.
