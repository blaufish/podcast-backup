import argparse
import feedparser
import logging
import os
import re
import requests

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

def create_dir(fdir):
    if not os.path.exists(fdir):
        logging.debug(f"mkdir: {fdir}")
        os.mkdir(fdir)

#
# Utility functions
#

def gimme_mp3(links):
    yolo = None
    for link in links:
        href = link['href']
        if href.endswith('.mp3'):
            return href
        else:
            yolo = href
    return yolo

def generate_yyyy_mm_dirname(basename, ts):
    yyyy = str(ts.tm_year)
    mm = str(ts.tm_mon)
    if len(mm) == 1:
        mm = "0" + mm
    ddir = os.path.join(basename, yyyy)
    create_dir(ddir)
    ddir = os.path.join(ddir, mm)
    create_dir(ddir)
    return ddir

def yyyymmdd(ts):
    yyyy = str(ts.tm_year)
    mm = str(ts.tm_mon)
    dd = str(ts.tm_mday)
    if len(mm) == 1:
        mm = "0" + mm
    if len(dd) == 1:
        dd = "0" + dd
    return yyyy + mm + dd

def sanitize_filename(fn):
    fn = fn.lower()
    fn = fn.replace('å','a')
    fn = fn.replace('ä','a')
    fn = fn.replace('ö','o')
    fn = fn.replace('Å','A')
    fn = fn.replace('Ä','A')
    fn = fn.replace('Ö','O')
    fn = re.sub('[^a-zA-Z0-9]+', '_', fn)
    fn = fn.strip('_')
    fn = re.sub('_mp3$', '.mp3', fn)
    return fn

def generate_filename(title, mp3, ts):
    # Dirname: basedir/YYYY/MM/YYYYMMDD_Title
    ddir = generate_yyyy_mm_dirname(dir_backups, ts)
    fn = yyyymmdd( ts ) + "_" + title
    fn = sanitize_filename(fn)
    ddir = os.path.join(ddir, fn)
    create_dir( ddir )
    # Filename: mp3-filename
    fn = mp3.split('/')[-1]
    fn = fn.split('?')[0]
    fn = sanitize_filename(fn)
    ddir = os.path.join(ddir, fn)
    return ddir

def download(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def process_rss(url):
    logger.info(f"Request feed from {url}")
    rss = feedparser.parse(url)
    entries = rss['entries'];
    for entry in entries:
        process_entry(entry)

def process_entry(e):
    published_p  = e['published_parsed']
    title        = e['title']
    links        = e['links']

    mp3 = gimme_mp3(links)
    fname = generate_filename(title, mp3, published_p)
    if os.path.exists(fname):
        logger.debug(f"Download: {fname} : Allready downloaded.")
    else:
        logger.info(f"Download: {fname}")
        download(mp3, fname)

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
            help = f'Directory to backup to. Writes files to dir/YYYY/MM/YYYYMMDD_Title/name.mp3')
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
