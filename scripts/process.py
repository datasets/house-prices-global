import os
import json
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from pprint import pprint
from datapackage import Package

source = 'https://www.bis.org/statistics/full_bis_selected_pp_csv.zip'
os.chdir('../')  # go to root datapackage folder

# read datapackage.json to use the metadata from it later
with open('datapackage.json') as file:
    datapackage_json = json.load(file)

# download and unzip source file
with urlopen(source) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        archived_files = zfile.namelist()
        zfile.extractall('archive/')

# pivot csv table
package = Package()
package.infer('archive/'+archived_files[0])
pprint(package.descriptor)
