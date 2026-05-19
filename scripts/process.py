import csv
import io
import os
import urllib.request

source_url = 'https://stats.bis.org/api/v2/data/dataflow/BIS/WS_SPP/1.0?format=csv&labels=both'


def parse_date(date):
    """Transforms BIS quarter format '1999-Q1' to ISO date '1999-03-31'."""
    return date.replace('Q1', '03-31').replace('Q2', '06-30').replace('Q3', '09-30').replace('Q4', '12-31')


def fetch():
    with urllib.request.urlopen(source_url) as response:
        return response.read().decode('utf-8')


def parse(content):
    """Read long-format CSV from the BIS SDMX API and split into 4 output files."""
    buckets = {
        'nominal_index': [],
        'nominal_year': [],
        'real_index': [],
        'real_year': [],
    }

    for row in csv.DictReader(io.StringIO(content)):
        value = row['Value']
        unit = row['Unit of measure']

        if 'Nominal' in value and 'Index' in unit:
            category = 'nominal_index'
        elif 'Nominal' in value and 'Year' in unit:
            category = 'nominal_year'
        elif 'Real' in value and 'Index' in unit:
            category = 'real_index'
        elif 'Real' in value and 'Year' in unit:
            category = 'real_year'
        else:
            continue

        buckets[category].append((
            parse_date(row['TIME_PERIOD']),
            row['REF_AREA'],
            row['Reference area'],
            row['OBS_VALUE'],
        ))

    os.makedirs('data', exist_ok=True)

    for name, rows in buckets.items():
        rows.sort()  # sorts by (date, country_code)
        with open(f'data/{name}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'country_code', 'country', 'price'])
            writer.writerows(rows)


if __name__ == '__main__':
    parse(fetch())
