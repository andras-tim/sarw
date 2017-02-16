#!/usr/bin/env python

import json
import os
import feedparser
from urlparse import urlparse, urljoin
from base_wallpaper_downloader import BaseWallpaperDownloader


class DownloadDoubleWideWallpaperFromWallpaperswide(BaseWallpaperDownloader):
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    LINKS_PATH = os.path.join(BASEDIR, 'wallpaperswide-old-links.json')
    FEED_URL = 'http://wallpaperswide.com/rss/3840x1080-wallpapers-r'

    def _download_image(self, destination_path):
        self._print_state('Reading list of old wallpapers...')
        old_links = set()
        if os.path.isfile(self.LINKS_PATH):
            with open(self.LINKS_PATH, 'r') as fd:
                old_links = set(json.load(fd) or [])
        self._print_state(' [{}]\n'.format(len(old_links)))

        self._print_state('Fetching new wallpapers... {query!r} '.format(query=str(self.FEED_URL)))
        feed_links = {
            urljoin(entry['link'], u'download{}-wallpaper-3840x1080.jpg'.format(urlparse(entry['link']).path[:-16]))
            for entry
            in feedparser.parse(self.FEED_URL)['entries']
        }
        new_links = sorted(feed_links.difference(old_links.intersection(feed_links)))
        self._print_state(' [{} new]\n'.format(len(new_links)))

        image_url = new_links[0]
        self._print_state('Downloading wallpaper... {!r} >> {!r} '.format(image_url, destination_path))
        file_size_kb = self._download_file(image_url, destination_path)
        self._print_state('[{} kb]\n'.format(file_size_kb))
        old_links.add(image_url)

        self._print_state('Updating list of old wallpapers...')
        with open(self.LINKS_PATH, 'w') as fd:
            json.dump(list(old_links), fd)
        self._print_state(' [{}]\n'.format(len(old_links)))


if __name__ == '__main__':
    DownloadDoubleWideWallpaperFromWallpaperswide().main()
