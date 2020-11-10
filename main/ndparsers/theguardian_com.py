from bs4 import BeautifulSoup
from . import ndutils

log = ndutils.log


def parse(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")
    author = ""
    title = soup.select("title")[0].text

    for p in soup.select("p"):
        # put hrefs into text form cause hrefs are important content
        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(ndutils.normspace(p.text))

    return title, author, ndutils.normspace([title] + text)
