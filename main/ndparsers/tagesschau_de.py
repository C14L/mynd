from bs4 import BeautifulSoup
from . import ndutils

log = ndutils.log


def parse(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")

    try:
        title = soup.select("title")[0].text.replace(" | tagesschau.de", "")
    except Exception:
        title = "No title tag"

    author = ""

    article = soup.select_one("#content")

    if not article:
        return title, author, ""

    try:
        text.append(article.select("span.dachzeile")[0].text)
    except Exception:
        pass

    try:
        text.append(article.select("span.headline")[0].text)
    except Exception:
        pass

    try:
        text.append(article.select("span.text span.stand")[0].text)
    except Exception:
        pass

    for p in article.select(".sectionArticle p"):
        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(p.text)

    return title, author, ndutils.normspace([title] + text)
