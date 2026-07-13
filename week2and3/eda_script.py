 #save filtered dataset as new csv.

import pandas as pd
sold = pd.read_csv("./input_data/combined_sold_residential.csv")

print("Rows: ", sold.shape[0])
print("Columns: ", sold.shape[1])

unique_property_types = sold['PropertyType'].unique()
print("Property types: ", unique_property_types)

sold = sold[sold.PropertyType == 'Residential']

df = pd.DataFrame(sold)
null_summary = pd.DataFrame({
    "Null Count": df.isnull().sum(),
    "Null Percentage": (df.isnull().sum() / len(df)) * 100
})

print(null_summary)

missing_value_report = pd.DataFrame({
    "Missing Percentage": (df.isnull().sum() / len(df)) * 100

})
missing_value_report = missing_value_report.sort_values(
    by="Missing Percentage",
    ascending=False
)

missing_value_report["To Drop"] = missing_value_report["Missing Percentage"] > 90

high_missing = (
    missing_value_report[missing_value_report["Missing Percentage"] > 90]
    [["Missing Percentage"]]
    .reset_index()
)

high_missing = high_missing.rename(columns={"index": "Column Name"})

print(high_missing)

print("Statistical summary for key columns:")
print(df[["ClosePrice", "LivingArea", "DaysOnMarket"]].describe())


sold.to_csv("outputs/filtered_sold_eda.csv", index=False)
missing_value_report.to_csv("high_missing_columns.csv", index=False)