import urllib2
import zipfile
from tabulator import Stream
from csv import writer

source_url = 'https://www.bis.org/statistics/full_bis_selected_pp_csv.zip'


def download_source():
    """ Downloads and unzip the source csv file
    :return: filename """
    u = urllib2.urlopen(source_url)
    with open('archive/source.zip', 'wb') as f:
        f.write(u.read())

    with zipfile.ZipFile('archive/source.zip') as zfile:
        zfile.extractall('archive/')
        return 'archive/' + zfile.namelist()[0]


def parse_date(date):
    """ transforms date from quartals '1999-Q1' to usual '1999-03-31' """
    return date.replace('Q1', '03-31').replace('Q2', '06-30').replace('Q3', '09-30').replace('Q4', '12-31')


def parse(filename):
    """ Read csv file and parse it into 4 different csv files with unpivoted data."""
    input_table = Stream(filename, skip_rows=[1, 2, 3, 4, 5]).open().read()
    headers = input_table.pop(0)
    dates = headers[5:]

    output = {
        # "description": "Nominal Index, 2010 = 100",
        "nominal_index": writer(open('data/nominal_index.csv', 'wb')),
        # "description": "Nominal Year-on-year changes, in per cent",
        "nominal_year": writer(open('data/nominal_year.csv', 'wb')),
        # "description": "Real Index, 2010 = 100",
        "real_index": writer(open('data/real_index.csv', 'wb')),
        # "description": "Real Year-on-year changes, in per cent",
        "real_year": writer(open('data/real_year.csv', 'wb'))
    }

    # headers
    for csv_file in output.values():
        csv_file.writerow(['date', 'country', 'price'])

    # processing
    for date in dates:
        for row in input_table:
            country = row[1]
            value = row[2]
            unit = row[3]
            price = row[headers.index(date)]

            category = ''
            if 'Nominal' in value and 'Index' in unit:
                category = 'nominal_index'
            elif 'Nominal' in value and 'Year' in unit:
                category = 'nominal_year'
            elif 'Real' in value and 'Index' in unit:
                category = 'real_index'
            elif 'Real' in value and 'Year' in unit:
                category = 'real_year'

            output[category].writerow([parse_date(date), country[3:], price])


def extract_csv_structure():
    """helper function"""
    from datapackage import Package
    import json
    with open('structure.txt', 'w') as file:
        file.write(
            json.dumps(
                Package().infer('data/*.csv'),
                indent=2,
                sort_keys=True)
        )

if __name__ == "__main__":
    data_file = download_source()
    parse(data_file)
