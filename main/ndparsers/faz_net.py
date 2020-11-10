from main.ndutils import normspace
from bs4 import BeautifulSoup

from .. import ndutils

log = ndutils.log


def parse(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("title")[0].text
    author = ""
    article = soup.select("article.atc")[0]

    try:
        text.append(article.select("span.atc-HeadlineEmphasisText")[0].text)
    except Exception:
        pass

    try:
        text.append(article.select("span.atc-HeadlineText")[0].text)
    except Exception:
        pass

    try:
        text.append(
            "{} {}".format(
                article.select("span.atc-MetaTimeText")[0].text,
                article.select("time.atc-MetaTime")[0].text,
            )
        )
    except Exception:
        pass

    try:
        text.append(article.select("p.atc-ImageDescriptionText")[0].text)
    except Exception:
        pass

    try:
        text.append(article.select("p.atc-IntroText")[0].text)
    except Exception:
        pass

    for p in article.select("p.atc-TextParagraph"):
        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(p.text)

    return title, author, ndutils.normspace([title] + text)
