Residential property price statistics from different countries. Contains property price indicators (real series are the nominal price series deflated by the consumer price index), both in levels and in growth rates. Can be used for property market analysis.

## Data

 This data comes from [Bank For International Settlements BIS](http://www.bis.org/statistics/pp.htm).
 There are several series of data on the BIS site:
   - detailed data set. Format: xlsx
   - [source of this repo] selected series (nominal and real). Format: xlsx, csv. 
   - long series. Formats: xlsx, csv
   - Commercial property price series. Format: xlsx
 
Here we use *Selected series* set, reasons are: 

 - 'Selected series' dataset covers most of the countries
 - has the csv source https://www.bis.org/statistics/full_bis_selected_pp_csv.zip  
 - facilitates access for users and enhance comparability.

#### Data format

The csv table contains the date column and the price indicator columns.
 A column name looks like *Q:4T:N:771, Q:4T:R:628, Q:4T:R:771, Q:5R:N:628*.  
 Each column name encodes (example for "Q:AU:N:628"):
 - "Frequency": "Q:Quarterly",
 - "Reference area": "AU:Australia",
 - "Value": "N:Nominal",
 - "Unit of measure": "628:Index, 2010 = 100",
 
 Each column name detailed decoding is stored in the datapackage.json
  ('resources' > 'schema' > 'fields').  
  All this coding system is taken from and is equal to the Bank For International Settlements standards. 
  

#### Detailed Data Description:

Contains data for 59 countries at a quarterly frequency (real series are the nominal price series deflated by the consumer price index), both in levels and in growth rates (ie four series per country). These indicators have been selected from the detailed data set to facilitate access for users and enhance comparability. The BIS has made the selection based on the Handbook on Residential Property Prices and the experience and metadata of central banks. An analysis based on these selected indicators is also released on a quarterly basis, with a particular focus on longer-term developments in the May release.

## Preparation 
You will need python3 installed to run the data downloading and processing script.
``` bash
git clone https://github.com/datasets/global-house-prices.git
cd global-house-prices
python3 scripts/process.py
```

## license

Sources: National sources, BIS Residential Property Price database, www.bis.org/statistics/pp.htm.