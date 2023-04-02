import argparse
import datetime
import feedparser
import logging
import os
import re
import time
import yaml

#
# Global variables, arguments
#

logger = None
dir_backups = None

#
# Setters for global variables
# May also include some basic input validation
#

def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format = FORMAT)

def dir_setup(fdir):
    global dir_backups
    if not os.path.exists(fdir):
        raise Exception(f"Directory {fdir} does not exists.")
    dir_backups = fdir

#
# Utility functions
#

def timestruct_to_isoformat(ts):
    t = time.mktime(ts)
    dt = datetime.datetime.fromtimestamp(t)
    iso = dt.isoformat()
    return iso

def gimme_mp3(links):
    yolo = None
    for link in links:
        href = link['href']
        if href.endswith('.mp3'):
            return href
        else:
            yolo = href
    return yolo

def generate_filename(title):
    fn = title
    fn = fn.lower()
    fn = fn.replace('å','a')
    fn = fn.replace('ä','a')
    fn = fn.replace('ö','o')
    fn = fn.replace('Å','A')
    fn = fn.replace('Ä','A')
    fn = fn.replace('Ö','O')
    fn = re.sub('[^a-zA-Z0-9]+', '_', fn)
    fn = fn.strip('_')
    return fn

def process_rss(url):
    logger.info(f"Request feed from {url}")
    rss = feedparser.parse(url)
    entries = rss['entries'];
    for entry in entries:
        process_entry(entry)

def process_entry(e):
    published    = e['published']
    published_p  = e['published_parsed']
    title        = e['title']

    fname = generate_filename(title)
    fname_full = dir_backups + "/" + fname

    summary      = e['summary']
    duration     = e['itunes_duration']
    links        = e['links']
    published_pp = timestruct_to_isoformat( published_p )
    mp3 = gimme_mp3(links)
    logger.info(f"MP3: {mp3}")

    logger.info(f"Update: {fname_full}")

def main():
    parser = argparse.ArgumentParser(
            prog = 'podcast.backup.py',
            description = 'Libsyn RSS to Mp3 backup (alpha quality)',
            epilog = 'Hope this help was helpful! :-)')
    #
    # Required arguments
    #
    parser.add_argument('--dir',
            dest = 'dir',
            default = None,
            required = True,
            help = f'Hugo posts directory (where to write files to).')
    parser.add_argument('--url',
            dest = 'url',
            required = True,
            help = 'URL to lib-syn RSS feed, e.g. https://sakerhetspodcasten.libsyn.com/rss')
    #
    # Optional arguments
    #
    parser.add_argument('--loglevel',
            dest = 'loglevel',
            default = 'INFO',
            choices = ['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()
    #
    # Set and validate globals
    #
    logging_setup(args.loglevel)
    dir_setup(args.dir)
    #
    # Actually run the program
    #
    process_rss(args.url)

if __name__ == "__main__":
    main()
