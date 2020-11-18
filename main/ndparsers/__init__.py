from . import ndutils, theguardian_com, tagesschau_de, faz_net, taz_de

log = ndutils.log


def get_parser(url: str):
    parsers = {
        "https://www.theguardian.com/": theguardian_com,
        "https://www.tagesschau.de/": tagesschau_de,
        "https://www.faz.net/": faz_net,
        "https://taz.de/": taz_de,
    }

    for (domain, module) in parsers.items():
        if url.startswith(domain):
            return module.parse

    raise RuntimeError("No parser configured for this domain.")
