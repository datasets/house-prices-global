import os
import json
import csv
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from pprint import pprint
from datapackage import Package

source_url = 'https://www.bis.org/statistics/full_bis_selected_pp_csv.zip'
os.chdir('../')  # go to root datapackage folder

# read datapackage.json to use the metadata from it later
with open('datapackage.json') as file:
    datapackage_json = json.load(file)

def download_source(url):
    """
    Downloads zip file, unzip and saves csv file
    :return: filename
    """
    with urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            archived_files = zfile.namelist()
            zfile.extractall('archive/')

    print('source file downloaded and saved:', 'archive/' + archived_files[0])
    return 'archive/' + archived_files[0]  # now there is only one file in a source zip


def parse_csv(file):
    """

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
    print(table[0])
    for col_index in range(len(table[0])):
        pivoted.append([row[col_index] for row in table])

    return pivoted


def write_data(table, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)


if __name__ == '__main__':
    source_file_name = download_source(source_url)
    original_table = parse_csv(source_file_name)
    clean_table = original_table[5:]
    out_table = pivot_table(clean_table)
    out_file_name = 'data/data.csv'
    write_data(out_table, out_file_name)

    retrieved_date = original_table[1][1]
    #update_metadata(out_file_name, retrieved_date)
    # extract table header (column names)
    # package = Package()
    # package.infer('archive/'+archived_files[0])
    # pprint(package.descriptor)
