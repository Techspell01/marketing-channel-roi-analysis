-- Marketing Channel ROI Analysis — BigQuery Queries
-- Dataset: bigquery-public-data.google_analytics_sample.ga_sessions_*
-- (Real, obfuscated GA360 e-commerce session data from the Google Merchandise Store)

-- Query 1: Quick single-day test query
SELECT
  channelGrouping,
  COUNT(*) AS row_count
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
GROUP BY
  channelGrouping;


-- Query 2: Full year — sessions, transactions, revenue, conversion rate by channel
SELECT
  channelGrouping,
  COUNT(DISTINCT CONCAT(fullVisitorId, CAST(visitId AS STRING))) AS sessions,
  SUM(totals.transactions) AS transactions,
  SUM(totals.totalTransactionRevenue) / 1e6 AS revenue_usd,
  SAFE_DIVIDE(
    SUM(totals.transactions),
    COUNT(DISTINCT CONCAT(fullVisitorId, CAST(visitId AS STRING)))
  ) AS conversion_rate
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20160801' AND '20170801'
GROUP BY
  channelGrouping
ORDER BY
  revenue_usd DESC;

-- Results (Aug 2016 - Aug 2017):
-- Referral        104,701 sessions | 5,543 transactions | $717,600.25 | 5.294% conversion
-- Direct          142,856 sessions | 2,219 transactions | $498,530.03 | 1.553% conversion
-- Organic Search  381,137 sessions | 3,581 transactions | $377,075.81 | 0.940% conversion
-- Display           6,259 sessions |   152 transactions | $130,336.56 | 2.429% conversion
-- Paid Search      25,290 sessions |   479 transactions |  $47,543.43 | 1.894% conversion
-- Social          226,020 sessions |   131 transactions |   $8,396.78 | 0.058% conversion
-- Affiliates       16,372 sessions |     9 transactions |     $654.38 | 0.055% conversion
-- (Other)             120 sessions |     1 transaction  |      $11.99 | 0.833% conversion
