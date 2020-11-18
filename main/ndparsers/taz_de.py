from bs4 import BeautifulSoup
from . import ndutils

log = ndutils.log


def parse(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")

    try:
        title = soup.select_one("title").text.replace(" - taz.de", "")
    except Exception:
        title = "No title tag"

    author = ""

    article = soup.select_one('article[itemprop="articleBody"]')

    if not article:
        return title, author, ""

    for p in article.select("p.article"):
        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(p.text)

    return title, author, ndutils.normspace([title] + text)
