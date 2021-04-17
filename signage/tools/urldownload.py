import urllib.parse
import os
from pathlib import Path
import requests
from datetime import datetime
import re

def download(url, output_directory: Path):
    try:
        response = requests.get(url, allow_redirects=True, stream = True)
    except Exception as e:
        print("{} urldownload requests.get Exception {}".format(datetime.now(), e))
        return None
    if response.status_code != 200:
        print("{} urldownload requests.get status_code {}: {}".format(datetime.now(), response.status_code, url))
        return None
        
    filename = _detect_filename(url, response.headers)
    if filename is None:
        print("{} urldownload filename not detected: {}, {}".format(datetime.now(), url, response.headers))
        return None
    output_file = output_directory / filename

    try:
        with output_file.open(mode='wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_file
    except Exception as e:
        print("{} urldownload '{}' write '{}' Exception {}".format(datetime.now(), url, output_file, e))
        return None

def _detect_filename(url=None, headers=None):
    names = dict(url='', headers='')
    if url:
        names["url"] = _filename_from_url(url) or ''
    if headers:
        names["headers"] = _filename_from_headers(headers) or ''
    return names["headers"] or names["url"] or None

def _filename_from_url(url):
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname

def _filename_from_headers(headers):
    cdisp = headers.get("Content-Disposition")
    if not cdisp:
        return None
    fnames = re.findall("filename\*?=['\"]?(?:UTF-\d['\"]*)?([^;\r\n\"]*)['\"]?;?", cdisp)
    for fname in fnames:
        if fname:
            return fname
    return None
