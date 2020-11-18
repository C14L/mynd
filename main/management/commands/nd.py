#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from time import sleep

from main import ndparsers
from main.ndparsers import ndutils
from main.models import PageUrl, PageText

log = ndutils.log

TIMEDELTA_BETWEEN_VERSION = timedelta(days=1)
TIMEDELTA_BETWEEN_POLLS = timedelta(seconds=3)


class Command(BaseCommand):
    help = "Poll a URL."

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, default="", help="URL to poll.")
        parser.add_argument("--all", action="store_true", help="Poll all URLs.")
        parser.add_argument("--dryrun", action="store_true", help="Don't write to DB.")
        parser.add_argument("--force", action="store_true", help="Poll now.")

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        is_all = kwargs["all"]
        is_dryrun = kwargs["dryrun"]
        is_force = kwargs["force"]

        if url:
            ndparsers.get_parser(url)  # Make sure URL is on a known domain.
            if is_dryrun:
                page_url = PageUrl(url=url)
            else:
                page_url, created = PageUrl.objects.get_or_create(url=url)
                if created:
                    print("New URL was added to PageUrl table.")
                else:
                    print("Known URL loaded from PageUrl table.")
            page_urls = [page_url]
        else:
            tlim = datetime.now(timezone.utc) - TIMEDELTA_BETWEEN_VERSION
            query = PageUrl.objects.filter(is_active=True)
            query = query.order_by("-last_polled_on")

            if not is_force:
                query = query.filter(Q(last_polled_on__lt=tlim)|Q(last_polled_on=None))

            if not is_all:
                query = query[:1]

            page_urls = query
            print("URLs loaded.")

        for page_url in page_urls:
            print("URL: %s" % page_url.url)
            if not is_dryrun:
                sleep(TIMEDELTA_BETWEEN_POLLS.seconds)

            html, err = ndutils.fetch(page_url.url)

            if err:
                page_url.last_error_on = datetime.now(timezone.utc)
                page_url.last_error_description = "Fetch error: %s" % err
                page_url.save()
                continue

            log.debug("Fetched %d Bytes of HTML.", len(html))

            page_text = PageText(url=page_url, html=html)
            page_url.last_polled_on = ndutils.now()

            try:
                title, author, content = ndparsers.get_parser(page_url.url)(page_text.html)
            except Exception as exc:
                page_url.last_error_on = datetime.now(timezone.utc)
                page_url.last_error_description = \
                    "Parse error: %s" % getattr(exc, 'message', repr(exc))
                page_url.save()
                continue

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
