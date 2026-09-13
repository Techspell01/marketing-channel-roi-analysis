import pandas as pd
df = pd.read_csv("marketing_campaigns.csv")

print("Raw shape:", df.shape)
print(df.head())
print(df.dtypes)

print("\nMissing values per column:")
print(df.isnull().sum())

before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows")

df["Start_Date"] = pd.to_datetime(df["Start_Date"])
df["End_Date"] = pd.to_datetime(df["End_Date"])
df["Duration_Days"] = (df["End_Date"] - df["Start_Date"]).dt.days

suspicious = df[(df["Total_Spend"] <= 0) | (df["Revenue_Generated"] < 0)]
print(f"\nSuspicious rows (zero/negative spend or negative revenue): {len(suspicious)}")
if len(suspicious) > 0:
    print(suspicious)
    df = df.drop(suspicious.index)
    
df["ROI"] = (df["Revenue_Generated"] - df["Total_Spend"]) / df["Total_Spend"]
df["CTR"] = df["Clicks"] / df["Impressions"]                
df["Conversion_Rate"] = df["Conversions"] / df["Clicks"]     
df["CPA"] = df["Total_Spend"] / df["Conversions"]            

for col in ["ROI", "CTR", "Conversion_Rate", "CPA"]:
    df[col] = df[col].round(3)

print("\nSample with KPIs:")
print(df[["Campaign_Name", "Marketing_Channel", "Total_Spend",
          "Revenue_Generated", "ROI", "CTR", "Conversion_Rate", "CPA"]].head(10))

df.to_csv("marketing_campaigns_clean.csv", index=False)
print("\nSaved cleaned dataset to marketing_campaigns_clean.csv")
print("Final shape:", df.shape)
