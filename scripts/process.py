import urllib.request
import zipfile
import csv
import os
from frictionless import Resource

source_url = 'https://www.bis.org/statistics/full_spp_csv.zip'

def download_source():
    """ Downloads and unzip the source csv file
    :return: filename """
    os.makedirs('archive', exist_ok=True)
    
    with urllib.request.urlopen(source_url) as u, open('archive/source.zip', 'wb') as f:
        f.write(u.read())
    
    with zipfile.ZipFile('archive/source.zip', 'r') as zfile:
        zfile.extractall('archive/')
        return 'archive/' + zfile.namelist()[0]

def parse_date(date):
    """ Transforms date from quartals '1999-Q1' to usual '1999-03-31' """
    return date.replace('Q1', '03-31').replace('Q2', '06-30').replace('Q3', '09-30').replace('Q4', '12-31')

def parse(filename):
    """ Read csv file and parse it into 4 different csv files with unpivoted data."""
    resource = Resource(filename)
    data = resource.read_rows()
    headers = resource.header
    dates = headers[12:]

    os.makedirs('data', exist_ok=True)
    
    output = {
        "nominal_index": csv.writer(open('data/nominal_index.csv', 'w', newline='')),
        "nominal_year": csv.writer(open('data/nominal_year.csv', 'w', newline='')),
        "real_index": csv.writer(open('data/real_index.csv', 'w', newline='')),
        "real_year": csv.writer(open('data/real_year.csv', 'w', newline=''))
    }
    
    for csv_file in output.values():
        csv_file.writerow(['date', 'country_code', 'country', 'price'])
    
    for date in dates:
        for row in data:
            country_code = row['REF_AREA']
            country = row['Reference area']
            value = row['Value']
            unit = row['Unit of measure']
            price = row[date]
            
            category = ''
            if 'Nominal' in value and 'Index' in unit:
                category = 'nominal_index'
            elif 'Nominal' in value and 'Year' in unit:
                category = 'nominal_year'
            elif 'Real' in value and 'Index' in unit:
                category = 'real_index'
            elif 'Real' in value and 'Year' in unit:
                category = 'real_year'
            
            if category:
                output[category].writerow([parse_date(date), country_code, country, price])

def extract_csv_structure():
    """Helper function"""
    from frictionless import Package
    import json
    
    with open('structure.txt', 'w') as file:
        file.write(
            json.dumps(
                Package('data').to_descriptor(),
                indent=2,
                sort_keys=True
            )
        )

if __name__ == "__main__":
    data_file = download_source()
    print(data_file)
    parse(data_file)