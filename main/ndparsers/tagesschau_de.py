from bs4 import BeautifulSoup
from . import ndutils

log = ndutils.log


def parse(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("title")[0].text.replace(" | tagesschau.de", "")
    author = ""
    article = soup.select_one("#content")

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
        # if p.has_class("autorenzeile"):

        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(p.text)

    return title, author, ndutils.normspace([title] + text)
