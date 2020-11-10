#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from time import sleep

from main import ndparsers
from main.ndparsers import ndutils
from main.models import PageUrl, PageText

log = ndutils.log


class Command(BaseCommand):
    help = "Parse HTML into text only."

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, default="", help="URL to parse.")
        parser.add_argument("--all", action="store_true", help="Parse all stored HTML.")
        parser.add_argument("--dryrun", action="store_true", help="Don't write to DB.")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        is_all = kwargs["all"]
        is_dryrun = kwargs["dryrun"]

        if url:
            page_urls = [PageUrl.objects.get(url=url)]
        else:
            query = PageUrl.objects.filter(is_active=True)
            query = query.order_by("pk")
            if not is_all:
                query = query[:1]
            page_urls = query
            print("URLs loaded.")

        for page_url in page_urls:
            print("URL: %s" % page_url.url, end=" ")

            for page_text in page_url.texts.all():
                html = ndutils.fetch(page_url.url)

                title, author, content = ndparsers.get_parser(page_url.url)(html)

                page_text.text = content
                page_url.title = title
                page_url.author = author
                page_url.last_parsed_on = ndutils.now()
                log.debug("Parsed into %d Bytes of text.", len(page_text.text))

                if is_dryrun:
                    print("DRYRUN")
                    print("-" * 60)
                    print(
                        page_text.text.replace(" ", "·")
                        .replace("\r", "␍\r")
                        .replace("\n", "⏎\n")
                    )
                    print("-" * 60)
                else:
                    page_text.save()
                    page_url.save()
                    print(".", end="", flush=True)
            print("")
