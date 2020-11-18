import datetime
import hashlib
import logging
import requests
import sys

logging.basicConfig(level=logging.INFO)
logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)


def strip_whitespace(text):
    lines = text.split("\n")
    return "\n".join(x.strip().rstrip(u"\xa0") for x in lines).strip() + "\n"


def concat_domain_url(domain, url):
    return domain + url if url.startswith("/") else domain + "/" + url


def fetch(url):
    err = None
    req = requests.Session()
    res = req.get(url)
    res.raise_for_status()

    if res.history:
        if hostname(url) != hostname(res.url):
            return None, "Redirects to other host: %s" % res.url

    content = res.content.decode()
    return content, err


def get_hash(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def normspace(t):
    """Normalize or remove redundant whitespace, tabs, etc anywhere in text."""
    # TODO: remove more stuff
    def do(x):
        if x:
            return " ".join(x.strip().split())

    if isinstance(t, str):
        return do(t)

    res = [do(x) for x in t]
    res = [x for x in res if x]
    res = "\n\n".join(res)

    return res


def hostname(url):
    return (
        url.split("//")[-1]
        .split("/")[0]
        .split("?")[0]
        .split(":")[0]
        .lower()
        .replace("www.", "")
    )
