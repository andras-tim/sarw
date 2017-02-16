#!/usr/bin/env python

import random
import requests
from datetime import date, timedelta
from lxml import etree
from urlparse import urlparse, parse_qsl
from base_wallpaper_downloader import BaseWallpaperDownloader


class DownloadDoubleWideWallpaperFromGoogle(BaseWallpaperDownloader):
    MIN_FILE_SIZE_KB = 500

    def _download_image(self, destination_path):
        query = 'dual background OR wallpaper'
        if self._options:
            query = self._options[0]

        self._print_state('Fetching wallpapers... {query!r} '.format(query=query))
        response = self._search_for_image(query=query, safe=True, photo_only=True, width=2 * 1920, height=1080,
                                          age_days=30)
        images = self._parse_images(response.content)
        self._print_state('>> {} pcs\n'.format(len(images)))

        while True:
            random_image = random.choice(images)
            self._print_state('Downloading wallpaper... {!r} >> {!r} '.format(random_image['url'], destination_path))
            file_size_kb = self._download_file(random_image['url'], destination_path, random_image['referer'])
            self._print_state('[{} kb]\n'.format(file_size_kb))

            if file_size_kb >= self.MIN_FILE_SIZE_KB:
                break
            self._print_state('File size is too low; min={}\n\n'.format(self.MIN_FILE_SIZE_KB))

    def _parse_images(self, html):
        images_xpath = './/div/a'
        image_url_xpath = './@href'

        xml = etree.fromstring(html, parser=etree.HTMLParser())

        results = []
        for image_element in xml.xpath(images_xpath):
            urls = image_element.xpath(image_url_xpath)
            if not urls:
                continue

            split_url = urlparse(urls[0])
            if not split_url.path == '/imgres':
                continue

            query = dict(parse_qsl(split_url.query))

            results.append({
                'referer': query['imgrefurl'],
                'url': query['imgurl'],
            })

        return results

    def _search_for_image(self, query, safe=False, photo_only=False, width=None, height=None, age_days=None):
        query_params = {
            'q': query,
            'safe': 'on' if safe else 'off',
            'site': 'webhp',
            'tbm': 'isch',
            'source': 'lnt',
            'tbs': ','.join(['{}:{}'.format(k, v) for k, v in self._get_image_params(photo_only, width, height, age_days).items()])
        }

        headers = {
            'User-Agent': self.USER_AGENT,
            'Referer': 'https://www.google.com',
        }

        return requests.get('https://www.google.com/search', params=query_params, headers=headers)

    def _get_image_params(self, photo_only=False, width=None, height=None, age_days=None):
        params = {}

        if photo_only:
            params['itp'] = 'photo'

        if not width:
            width = height
        if not height:
            height = width
        if height and width:
            params['isz'] = 'ex'
            params['iszw'] = width
            params['iszh'] = height

        if age_days:
            today = date.today()
            params['cdr'] = 1
            params['cd_min'] = self._format_date(today - timedelta(days=age_days))
            params['cd_max'] = self._format_date(today)

        return params

    def _format_date(self, date):
        return date.strftime('%Y. %m. %d.')


if __name__ == '__main__':
    DownloadDoubleWideWallpaperFromGoogle().main()
