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
 A column name consist of four fields and looks like this: *Q:4T:N:771, Q:4T:R:628, Q:4T:R:771, Q:5R:N:628, Q:AU:N:628*.  
 #### column name format 
 The column name encodes information about the:
 - "Frequency": could be *Q:Quarterly*,
 - "Reference area": could be *4T:Emerging market economies* or *5R:Advanced economies* or some country code, e.g. *AU:Australia*),
 - "Value": could be *N:Nominal* or *R:Real*,
 - "Unit of measure": could be *771:Year-on-year changes, in per cent* or *628:Index, 2010 = 100*, or another, depending of the base year (mostly 2010)
 
 Each column name is decoded in the datapackage.json ( in the 'resources' > 'schema' > 'fields'), e.g. 
```json
{
  "Frequency": "Q:Quarterly",
  "Reference area": "AE:United Arab Emirates",
  "Unit of measure": "771:Year-on-year changes, in per cent",
  "Value": "N:Nominal",
  "name": "Q:AE:N:771"
}
```
which is useful for extracting this data in your programs.  

The coding system is taken from and is equal to the Bank For International Settlements standards. 
  

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