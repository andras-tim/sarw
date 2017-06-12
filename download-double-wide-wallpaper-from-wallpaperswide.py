#!/usr/bin/env python

import json
import os
import random
import time
from urlparse import urlparse, urljoin
import requests
from lxml import etree

from base_wallpaper_downloader import BaseWallpaperDownloader


class DownloadDoubleWideWallpaperFromWallpaperswide(BaseWallpaperDownloader):
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    LINKS_PATH = os.path.join(BASEDIR, 'wallpaperswide-old-links.json')
    ROOT_URL = 'http://wallpaperswide.com/'
    PAGE_BASE_URL = urljoin(ROOT_URL, '3840x1080-wallpapers-r/page/')
    MAX_PAGES = 500
    MAX_FETCH_TRIES = 5

    def _download_image(self, destination_path):
        self._print_state('Reading list of old wallpapers...')
        old_links = set()
        if os.path.isfile(self.LINKS_PATH):
            with open(self.LINKS_PATH, 'r') as fd:
                old_links = set(json.load(fd) or [])
        self._print_state(' [{}]\n'.format(len(old_links)))

        new_links = self.__fetch_new_wallpapers(old_links)

        image_url = new_links[0]
        self._print_state('Downloading wallpaper... {!r} >> {!r} '.format(image_url, destination_path))
        file_size_kb = self._download_file(image_url, destination_path)
        self._print_state('[{} kb]\n'.format(file_size_kb))
        old_links.add(image_url)

        self._print_state('Updating list of old wallpapers...')
        with open(self.LINKS_PATH, 'w') as fd:
            json.dump(list(old_links), fd)
        self._print_state(' [{}]\n'.format(len(old_links)))

    def __fetch_new_wallpapers(self, old_links):
        random.seed()
        for _ in xrange(self.MAX_FETCH_TRIES):
            new_links = self.__fetch_page_for_new_wallpapers(old_links)
            if new_links:
                return new_links
            time.sleep(0.3)

        raise Exception('Can not fetch new wallpapers')

    def __fetch_page_for_new_wallpapers(self, old_links):
        page = random.randrange(self.MAX_PAGES)
        page_url = urljoin(self.PAGE_BASE_URL, u'{}'.format(page))

        self._print_state('Fetching wallpapers... {query!r} '.format(query=str(page_url)))

        response = requests.get(page_url)
        page_links = self.__parse_images(response.content)

        new_links = sorted(page_links.difference(old_links.intersection(page_links)))
        self._print_state(' [{} new]\n'.format(len(new_links)))

        return new_links

    def __parse_images(self, html):
        image_link_xpath = './/ul[@class="wallpapers"]/li[@class="wall"]/div[@class="thumb"]/a'

        xml = etree.fromstring(html, parser=etree.HTMLParser())

        results = set()
        for image_link_elements in xml.xpath(image_link_xpath):
            image_page_urls = image_link_elements.xpath('./@href')
            if not image_page_urls:
                continue

            image_url = u'download{}-wallpaper-3840x1080.jpg'.format(urlparse(image_page_urls[0]).path[:-16])
            results.add(urljoin(self.ROOT_URL, image_url))
        return results


if __name__ == '__main__':
    DownloadDoubleWideWallpaperFromWallpaperswide().main()
