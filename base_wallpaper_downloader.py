import os
import sys
import requests


class BaseWallpaperDownloader(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'

    def __init__(self):
        self._image_path = sys.argv[1]

        self._options = []
        if len(sys.argv) > 2:
            self._options = sys.argv[1:]

    def main(self):
        requests.packages.urllib3.disable_warnings()
        self._download_image(self._image_path)
        self._print_state('Done\n')

    def _download_image(self, destination_path):
        raise NotImplementedError

    def _download_file(self, url, destination_path, referer=None):
        headers = {
            'User-Agent': self.USER_AGENT,
        }
        if referer:
            headers['Referer'] = referer

        response = requests.get(url, headers=headers, stream=True, verify=False)
        with open(destination_path, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
            fd.flush()

        return os.path.getsize(destination_path) / 1024

    def _print_state(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()
