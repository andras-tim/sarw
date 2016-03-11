#!/usr/bin/env python

import random
import requests
import sys
from datetime import date, timedelta
from lxml import etree
from urlparse import urlparse, parse_qsl

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'


def main(*args):
    image_path = args[0]

    query = 'hd wallpaper'
    if len(args) > 1:
        query = args[1]

    print_state('Fetching wallpapers... ')
    response = search_for_image(query=query, safe=True, photo_only=True, width=2 * 1920, height=1080, age_days=30)
    images = parse_images(response.content)
    print_state('{}\n'.format(len(images)))

    random_image = random.choice(images)

    print_state('Downloading wallpaper... {!r} >> {!r}\n'.format(random_image['url'], image_path))
    download_image(random_image, image_path)
    print_state('Done\n')


def parse_images(html):
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


def search_for_image(query, safe=False, photo_only=False, width=None, height=None, age_days=None):
    query_params = {
        'q': query,
        'safe': 'on' if safe else 'off',
        'site': 'webhp',
        'tbm': 'isch',
        'source': 'lnt',
        'tbs': ','.join(['{}:{}'.format(k, v) for k, v in get_image_params(photo_only, width, height, age_days).items()])
    }

    headers = {
        'User-Agent': USER_AGENT,
        'Referer': 'https://www.google.com',
    }

    return requests.get('https://www.google.com/search', params=query_params, headers=headers)


def download_image(image, destination_path):
    headers = {
        'User-Agent': USER_AGENT,
        'Referer': image['referer'],
    }

    response = requests.get(image['url'], headers=headers, stream=True)
    with open(destination_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                fd.write(chunk)
        fd.flush()


def get_image_params(photo_only=False, width=None, height=None, age_days=None):
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
        params['cd_min'] = format_date(today - timedelta(days=age_days))
        params['cd_max'] = format_date(today)

    return params


def format_date(date):
    return date.strftime('%Y. %m. %d.')


def print_state(text):
    sys.stdout.write(text)
    sys.stdout.flush()


if __name__ == '__main__':
    main(*sys.argv[1:])
