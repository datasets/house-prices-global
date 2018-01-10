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

Output is four files with different metrics:
* `data/nominal_index.csv` Nominal Index, 2010 = 100 
* `data/nominal_year.csv` Nominal Year-on-year changes, in per cent
* `data/real_index.csv` Real Index, 2010 = 100
* `data/real_year.csv` Real Year-on-year changes, in per cent

Each file structure is like this:
```
date,country,price
2012-06-30,Philippines,114.5
2012-06-30,Poland,97.36
2012-06-30,Portugal,88.15
2012-06-30,Romania,84.61
2012-06-30,Serbia,96.48
2012-06-30,Russia,89.81
2012-06-30,Sweden,103.47
```

#### Detailed Data Description:

Contains data for 59 countries at a quarterly frequency (real series are the nominal price series deflated by the consumer price index), both in levels and in growth rates (ie four series per country). These indicators have been selected from the detailed data set to facilitate access for users and enhance comparability. The BIS has made the selection based on the Handbook on Residential Property Prices and the experience and metadata of central banks. An analysis based on these selected indicators is also released on a quarterly basis, with a particular focus on longer-term developments in the May release.

## Preparation

You will need `python` and `pip` installed to run the data downloading and processing script.

``` bash
# if you don't have "git" you can download and unzip the datapackage directly from this page.
git clone https://github.com/datasets/global-house-prices.git

cd global-house-prices
pip install tabulator
python scripts/process.py
```

## License

The data source is National sources, Bank for International Settlements ("BIS") Residential Property Price database, www.bis.org/statistics/pp.htm.  
You can use this data following BIS rules:  
https://www.bis.org/terms_conditions.htm#Copyright_and_Permissions  
https://www.bis.org/terms_statistics.htm
