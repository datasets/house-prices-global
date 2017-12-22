import urllib2
import zipfile


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


if __name__ == "__main__":
    print(download_source())