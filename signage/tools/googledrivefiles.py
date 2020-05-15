from datetime import datetime
from datetime import timedelta
from urllib.parse import urlencode
import requests
import json


class GoogleDriveFile:

    def __init__(self):
        self.description = ""
        self.created_time = datetime.now()
        self.mime_type = ""
        self.web_content_link = ""


class GoogleDriveFiles:

    def __init__(self, developer_key, cache):
        self.cache = cache
        self.cache_ttl = timedelta(minutes=30)
        self.developer_key = developer_key
        self.folder_id = ""

    def get_files(self):
        response_content = self._request_files()
        content = self.load_json(response_content)
        if content:
            for content_file in content.get("files", []):
                drive_file = GoogleDriveFile()
                drive_file.id = content_file.get("id", "")
                drive_file.name = content_file.get("name", "")
                drive_file.description = content_file.get("description", "")
                drive_file.created_time = content_file.get("createdTime", "")
                drive_file.mime_type = content_file.get("mimeType", "")
                drive_file.web_content_link = content_file.get("webContentLink", "")
                yield drive_file

    def load_json(self, content):
        try:
            if content:
                return json.loads(content.decode('utf-8'))
            return None
        except Exception as e:
            print("{} GoogleDriveFiles Exception {} ({})".format(datetime.now(), e, content))
            return None

    def _request_files(self):
        cache_item = self.cache.get(self.folder_id)
        if self._is_valid_cache_item(cache_item, True):
            return cache_item.value

        content = self._do_request_files(self.folder_id, self.developer_key)
        if self._is_valid_content(content):
            self.cache.set(self.folder_id, content)
            return content

        if self._is_valid_cache_item(cache_item, False):
            return cache_item.value  # expired, but don't care
        return None

    def _do_request_files(self, folder_id, developer_key):
        data = {
            "q": "'{}' in parents".format(folder_id),
            "fields": "files(id,name,description,createdTime,mimeType,webContentLink)",
            "orderBy": "createdTime",
            "key": developer_key
        }
        url = "https://www.googleapis.com/drive/v3/files?" + urlencode(data)
        response = requests.get(url)
        return response.content if response.ok else None

    def _is_valid_cache_item(self, cache_item, check_expired):
        if cache_item is None:
            return False
        elif check_expired and cache_item.is_expired(self.cache_ttl):
            return False
        return self._is_valid_content(cache_item.value)

    def _is_valid_content(self, content):
        if content is None:
            return False
        return True
