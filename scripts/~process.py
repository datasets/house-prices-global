#!/usr/bin/env python3
import os
import json
import csv
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

source_url = 'https://www.bis.org/statistics/full_bis_selected_pp_csv.zip'
#os.chdir('../')  # go to root datapackage folder


def download_source(url):
    """
    Downloads zip file, unzip and saves csv file
    :return: filename
    """
    with urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            archived_files = zfile.namelist()
            zfile.extractall('archive/')
    return 'archive/' + archived_files[0]  # now there is only one file in a source zip


def parse_csv(file):
    """
    Reads csv file and returns nested list, which forms a table ( data[rows][columns] )
    :param file: csv file to read
    :return: table
    """
    out = list()
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            out.append(row)
    return out


def pivot_table(table):
    """
    pivots the table with time period as index column
    :param table:
    :return table:
    """
    pivoted = []
    for col_index in range(len(table[0])):
        pivoted.append([row[col_index] for row in table])
    return pivoted


def save_data(table):
    """
    Write the csv file and returns the metadata structure for datapackage.json
    :param table: nested list[][] representing csv data. Example:
    Frequency	Q:Quarterly	Q:Quarterly	Q:Quarterly	Q:Quarterly	Q:Quarterly	Q:Quarterly
    Reference area	4T:Emerging market economies	4T:Emerging market economies	4T:Emerging market economies	4T:Emerging market economies	5R:Advanced economies	5R:Advanced economies
    Value	N:Nominal	N:Nominal	R:Real	R:Real	N:Nominal	N:Nominal
    Unit of measure	628:Index, 2010 = 100	771:Year-on-year changes, in per cent	628:Index, 2010 = 100	771:Year-on-year changes, in per cent	628:Index, 2010 = 100	771:Year-on-year changes, in per cent
    Time Period	Q:4T:N:628	Q:4T:N:771	Q:4T:R:628	Q:4T:R:771	Q:5R:N:628	Q:5R:N:771
    1966-Q1
    1966-Q2
    1966-Q3
    1966-Q4

    :return: 'resources' list which describes the csv file columns (will be stored in datapackage.json)
    """
    # saving data-containing rows
    with open("data/data.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table[4:]:
            writer.writerow(row)

    # creating the table schema for datapackage.json
    # first column in a table is a date and has simple description
    fields = [{'name': 'Time Period', 'type': 'string'}]

    # then we go through columns[1:] and create description for each column.
    for column_index in range(1, len(table[0])):
        name = table[4][column_index]  # Q:4T:N:628 - the column code from original csv file from bis.org
        frequency = table[0][column_index]  # in this file is always 'Q: Quarterly'
        reference_area = table[1][column_index]  # country or 'Emerging market economic', 'Advanced market economic',
        value = table[2][column_index]  # N:Nominal or R:Real
        unit = table[3][column_index]
        # human readable description for datahub.io
        description = "%s; %s value; unit of measure: %s" % (reference_area, value, unit)

        fields.append({
            "name": name,
            "Frequency": frequency,
            "Reference area": reference_area,
            "Value": value,
            "Unit of measure": unit,
            "description": description
        })

    # file description
    file_metadata = {
        "encoding": "utf-8",
        "format": "csv",
        "mediatype": "text/csv",
        "name": "data",
        "path": "data/data.csv",
        "profile": "tabular-data-resource",
        "schema": {'fields': fields}
    }
    return file_metadata

# replace 1997-Q1 with date 
quarterly = zip(*transposed[4:7])
    # 1947q1 etc
    def fixquarters(date):
        mapping = [
            ['q1', '-01-01'],
            ['q2', '-04-01'],
            ['q3', '-07-01'],
            ['q4', '-10-01']
        ]
        for x in mapping:
            date = date.replace(x[0], x[1])
        return str(date)
    quarterly = [ [fixquarters(r[0])] + list(r[1:]) for r in quarterly ]


if __name__ == '__main__':
    source_file_name = download_source(source_url)
    print('source file downloaded and saved.')

    original_table = parse_csv(source_file_name)
    clean_table = original_table[5:]
    print('the table is parsed and cleaned')

#	Don't do pivoting! the table is good without it
#    out_table = pivot_table(clean_table)
#    print('the table is pivoted')

    csv_metadata = save_data(out_table)  # this function saves the data.csv file
    print('the data is saved in csv')

    datapackage_json = {
        "name": "residential-property-price-statistics-from-different-countries",
        "title": "BIS Selected property prices",
        "description": "Contain data for 59 countries at a quarterly frequency (real series are the nominal price series deflated by the consumer price index), both in levels and in growth rates (ie four series per country). These indicators have been selected from the detailed data set to facilitate access for users and enhance comparability. The BIS has made the selection based on the Handbook on Residential Property Prices and the experience and metadata of central banks. An analysis based on these selected indicators is also released on a quarterly basis, with a particular focus on longer-term developments in the May release.",
        "Frequency": "Quarterly",
        "Retrieved Date": original_table[1][1],
        "sources": [
            {
                "title": "BIS Selected property prices",
                "name": "Bank For International Settlements BIS",
                "web": "https://www.bis.org/statistics/pp_selected.htm",
                "url": "https://www.bis.org/statistics/full_bis_selected_pp_csv.zip"
            }
        ],
        "resources": [csv_metadata]
    }

    # at last save the metadata
    with open('datapackage.json', 'w') as file:
        file.write(json.dumps(datapackage_json, indent=2, sort_keys=True))

    print('The metadata is saved. The work is finished.')
