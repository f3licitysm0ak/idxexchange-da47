import glob
import pandas as pd
import os

#create outputs directory if it doesn't already exist
os.makedirs("outputs", exist_ok=True)

#using glob to get the files efficiently
listing_file_pattern = "listings_data/CRMLSListing*.csv"
all_listing_files = glob.glob(listing_file_pattern)

sold_file_pattern = "sold_data/CRMLSSold*.csv"
all_sold_files = glob.glob(sold_file_pattern)

listing_files_list = []
sold_files_list = []

for file in all_listing_files:
    temp = pd.read_csv(file)
    listing_files_list.append(temp)

print("Total listing files:", len(all_listing_files))
concat_listings = pd.concat(listing_files_list)
print("Listings BEFORE filter:", len(concat_listings))

filtered_listings = concat_listings[concat_listings['PropertyType'] == 'Residential']
print("Listings AFTER Residential filter:", len(filtered_listings))


for file in all_sold_files:
    temp = pd.read_csv(file)
    if "_filled" in file:
        temp = temp.iloc[:, :-2]
    sold_files_list.append(temp)

print("Total sold files:", len(all_sold_files))
concat_sold = pd.concat(sold_files_list)
print("Sold BEFORE filter:", len(concat_sold))

filtered_sold = concat_sold[concat_sold['PropertyType'] == 'Residential']
print("Sold AFTER Residential filter:", len(filtered_sold));


filtered_listings.to_csv("outputs/combined_listings_residential.csv", index=False)
filtered_sold.to_csv("outputs/combined_sold_residential.csv", index=False)
