import calendar
import glob
import logging
import os
import textwrap
import time
import urllib
import datetime

import feedparser
import xkcd
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

PATH = os.getcwd() + "/res/images"
LOG = logging.getLogger(__name__)
logging.getLogger('PIL.PngImagePlugin').setLevel('ERROR')

def fetch_dilbert():
    today = datetime.date.today().strftime("%Y-%d-%m")
    try:
        res = urllib.request.urlopen("https://dilbert.com/strip/{}".format(today))
        if res.status == 200:
            soup = BeautifulSoup(res.read(), 'html.parser')
            url = "https:" + soup.select_one(".img-comic")['src']
            file_extension = urllib.request.urlopen(url).info().get_content_subtype()
            urllib.request.urlretrieve(url, PATH + "/dilbert-{}.{}".format(today, file_extension))
    except urllib.error.URLError as error:
        LOG.error(error)


def fetch_xkcd(count):
    try:
        latest_num = xkcd.getLatestComicNum()

        for num in range(latest_num - count + 1, latest_num + 1):
            comic = xkcd.getComic(num, silent=False)
            filepath = PATH + "/xkcd-{}-{}".format(comic.number, comic.getImageName())
            if not os.path.isfile(filepath):
                comic.download(output=PATH)
            else:
                LOG.debug("%s already exists. Skipping...", filepath)
    except urllib.error.URLError as error:
        LOG.error(error)

def fetch_dw_news(count):
    feed = feedparser.parse("https://rss.dw.com/xml/rss-en-top")
    if not feed.feed:
        return

    # download logo
    logo_path = PATH + "/dw-logo.png"
    urllib.request.urlretrieve(feed.feed.image.href, logo_path)
    feed_logo = Image.open(logo_path)

    for entry in feed.entries[:count]:
        path = PATH + "/dw-{}.png".format(entry.id)
        if os.path.isfile(path):
            LOG.debug("%s already exists. Skipping...", path)
            continue
        make_news_image(entry.title, entry.summary,
                        entry.published_parsed, feed.feed.title, feed_logo, path)

    os.remove(logo_path)


def make_news_image(title, text, date_gmt, feed_name, logo, path):
    """Generates an image out of a news article"""
    date = time.strftime("%a, %d %b %Y %H:%M",
                         time.localtime(calendar.timegm(date_gmt)))
    img = Image.new('RGBA', (796, 392), color=(255, 255, 255, 255))

    title_fnt = ImageFont.truetype(
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    text_fnt = ImageFont.truetype(
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)

    d = ImageDraw.Draw(img)
    title_lines = textwrap.wrap(title, 40)
    d.multiline_text((30, 30), "\n".join(title_lines),
                     font=title_fnt, fill=(0, 0, 0))
    y_offset = 0
    if len(title_lines) == 3:
        y_offset = 26
    d.text((30, 86 + y_offset), date,  font=text_fnt, fill=(80, 80, 80))
    d.multiline_text((30, 130 + y_offset), textwrap.fill(text, 60),
                     spacing=16, font=text_fnt, fill=(0, 0, 0))

    img.paste(logo, (20, img.height - logo.height - 6))
    d.text((20 + logo.width, img.height - 40),
           feed_name, font=text_fnt, fill=(80, 80, 80))

    img.save(path)


def remove_older_than(days, type_prefix):
    seconds = time.time() - days * 24 * 60 * 60
    files = (path for path in glob.glob(PATH + "/" + type_prefix + "*")
             if os.path.isfile(path) and os.path.getmtime(path) < seconds)
    for path in files:
        LOG.info("Removing: %s", path)
        os.remove(path)


def remove_oldest(limit, type_prefix):
    '''Remove oldest files (by time of modification). Keep limit amount of files.'''
    files = list(filter(os.path.isfile, glob.glob(
        PATH + "/" + type_prefix + "*")))
    files.sort(key=os.path.getmtime)
    if len(files) > limit:
        for path in files[:len(files) - limit]:
            LOG.info("Removing: %s", path)
            os.remove(path)
    else:
        LOG.info("Nothing to delete: %s/%s %s", len(files), limit, type_prefix)


def run():
    fetch_dilbert()
    fetch_dw_news(5)
    fetch_xkcd(5)
    remove_oldest(10, "dilbert")
    remove_oldest(10, "xkcd")
    remove_oldest(10, "dw")


if __name__ == "__main__":
    run()
