import datetime
import gzip
import hashlib
import logging
import os
import os.path as path
import requests
import sys
import time

logging.basicConfig(level=logging.DEBUG)
logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)

raw_html_path = "data/raw_html"
content_path = "data/content"


class NoPreviousContentException(Exception):
    pass


def strip_whitespace(text: str) -> str:
    lines = text.split("\n")
    return "\n".join(x.strip().rstrip(u"\xa0") for x in lines).strip() + "\n"


def concat_domain_url(domain: str, url: str) -> str:
    return domain + url if url.startswith("/") else domain + "/" + url


def get_hash(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def get_filename(url: str) -> str:
    url_hash = get_hash(url)
    url_time = int(time.time())
    return "%s.%s" % (url_hash, url_time)


def fetch(url: str, refresh: bool = False) -> str:
    fname = path.join(raw_html_path, get_filename(url))
    log.debug("Downloading URL: %s", url)
    log.debug("Writing to file: %s", fname)

    if not refresh and path.exists(fname):
        with gzip.open(fname, "rt") as fh:
            return fh.read()

    req = requests.Session()
    res = req.get(url)
    res.raise_for_status()
    content = res.content.decode()

    with gzip.open(fname, "wt") as fh:
        fh.write(content)

    return content


def get_latest_content(url):
    h = get_hash(url)
    ld = os.listdir(content_path)

    versions = [x for x in ld if x.startswith(h) and x.endswith(".html.gz")]
    if not versions:
        log.debug("No previous version found of this content.")
        raise NoPreviousContentException()
    versions.sort()

    fname = path.join(content_path, versions[-1])
    log.debug("Loading content file: %s", fname)
    with gzip.open(fname, "rt") as fh:
        return fh.read()


def now():
    return datetime.datetime.now(datetime.timezone.utc)
