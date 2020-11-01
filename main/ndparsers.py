from bs4 import BeautifulSoup

from . import ndutils

log = ndutils.log


def parse_tagesschau_de(html: str) -> str:
    text = list()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select("title")[0].text.replace(" | tagesschau.de", "")

    for p in soup.select("#content .sectionArticle p.text.small"):
        # put hrefs into text form cause hrefs are important content
        for x in p.select("a"):
            x.append(" [" + x.get("href", "") + "]")
        text.append(" ".join(p.text.strip().split()))

    return "\n\n".join([title] + text)


def get_parser(url: str):
    parsers = {
        "https://www.tagesschau.de/": parse_tagesschau_de,
    }

    for (domain, func) in parsers.items():
        if url.startswith(domain):
            return func

    raise RuntimeError("No parser configured for this domain.")
