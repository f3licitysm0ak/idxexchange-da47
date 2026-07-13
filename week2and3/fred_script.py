import pandas as pd

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
mortgage.groupby('year_month')['rate_30yr_fixed']
.mean()
.reset_index())

sold = pd.read_csv("./outputs/filtered_sold_eda.csv")
listings = pd.read_csv("./input_data/combined_listings_residential.csv")

sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')

sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

if (sold_with_rates['rate_30yr_fixed'].isnull().sum() == 0 
    and listings_with_rates['rate_30yr_fixed'].isnull().sum() == 0):
    print("No null rate values exist and merge completed successfully.")
else:
    print("WARNING: Some null values may exist and merge completed.")
print(
"Preview of new sol dataset: ",
sold_with_rates[
['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
].head()
)

sold_with_rates.to_csv("./outputs/sold_with_rates", index=False)
listings_with_rates.to_csv("./outputs/listings_with_rates", index=False)