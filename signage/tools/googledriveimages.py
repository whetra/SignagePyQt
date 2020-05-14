from pathlib import Path
from .urlimages import UrlImages
from .googledrivefiles import GoogleDriveFiles


class GoogleDriveImages():

    def __init__(self, folder_id, developer_key, images_directory: Path, cache):
        self._google_drive_files = GoogleDriveFiles(developer_key, cache)
        self._google_drive_files.folder_id = folder_id
        self.imageprovider = UrlImages(images_directory, cache)
        self.max_images = None  # None = all images

    def getimages(self):
        files = self._google_drive_files.get_files()
        for file in self._filtersort_files(files):
            filepath = self.imageprovider.getimage(file.web_content_link)
            if filepath:
                yield filepath, file.description

    def _filtersort_files(self, files):
        sorted_files = sorted(files, key=lambda file: file.created_time, reverse=True)  # reverse to get only last creaed images
        filtered_files = list(filter(lambda file: file.mime_type.startswith("image/"), sorted_files))
        reduced_files = filtered_files[:self.max_images]
        return sorted(reduced_files, key=lambda file: file.created_time, reverse=False)
