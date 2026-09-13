import pandas as pd
df = pd.read_csv("marketing_campaigns_v2.csv")
print("Raw shape:", df.shape)
print(df.head())
print(df.dtypes)
print("\nMissing values per column:")
print(df.isnull().sum())

before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows")

df["Acquisition_Cost"] = (
    df["Acquisition_Cost"]
    .replace('[\$,]', '', regex=True)
    .astype(float)
)

df["Duration_Days"] = df["Duration"].str.extract(r'(\d+)').astype(int)
df["Date"] = pd.to_datetime(df["Date"])
print("\nROI stats:")
print(df["ROI"].describe())
print("\nAcquisition_Cost stats:")
print(df["Acquisition_Cost"].describe())

df["CTR"] = (df["Clicks"] / df["Impressions"]).round(4)
df["Estimated_Conversions"] = (df["Clicks"] * df["Conversion_Rate"]).round(1)
df["Cost_Per_Click"] = (df["Acquisition_Cost"] / df["Clicks"]).round(2)

print("\nSample with cleaned columns:")
print(df[["Campaign_ID", "Channel_Used", "Campaign_Type", "Acquisition_Cost",
          "ROI", "CTR", "Conversion_Rate", "Duration_Days"]].head(10))

df.to_csv("marketing_campaigns_v2_clean.csv", index=False)
print("\nSaved cleaned dataset to marketing_campaigns_v2_clean.csv")
print("Final shape:", df.shape)
