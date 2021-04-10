import urllib.parse
import os
from pathlib import Path
import requests
from datetime import datetime

def download(url, output_directory: Path):
    filename = _filename_from_url(url)
    if filename is None:
        print("{} urldownload filename is None: {}".format(datetime.now(), url))
        return None

    output_file = output_directory / filename
    try:
        r = requests.get(url, stream = True)
    except Exception as e:
        print("{} urldownload Exception {}".format(datetime.now(), e))
        return None
    if r.status_code != 200:
        print("{} urldownload status_code {}: {}".format(datetime.now(), r.status_code, url))
        return None

    with open(output_file,'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_file

def _filename_from_url(url):
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname
