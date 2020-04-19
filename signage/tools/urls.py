class Urls:

    def __init__(self):
        self.urls = []

    def get_urls(self):
        for url in self.urls:
            yield url
