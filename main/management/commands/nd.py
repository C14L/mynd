#!/usr/bin/env python3

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from main import ndparsers
from main import ndutils
from main.models import PageUrl, PageText

log = ndutils.log


class Command(BaseCommand):
    help = "Poll a URL."

    def add_arguments(self, parser):
        parser.add_argument("--url", type=str, default="", help="URL to poll.")
        parser.add_argument(
            "--all", action="store_true", help="Poll and parse all URLs."
        )
        parser.add_argument(
            "--nopoll", action="store_true", help="Do not poll this URL now."
        )
        parser.add_argument(
            "--noparse", action="store_true", help="Do not parse HTML of this URL now.",
        )
        parser.add_argument(
            "--force", action="store_true", help="Re-parse all past HTML of this URL.",
        )

    def handle(self, *args, **kwargs):
        url = kwargs["url"]
        all_urls = kwargs["all"]
        nopoll = kwargs["nopoll"]
        noparse = kwargs["noparse"]
        force = kwargs["force"]

        if url:
            ndparsers.get_parser(url)  # Make sure the URL is on a known domain.
            page_url, created = PageUrl.objects.get_or_create(url=url)
            if created:
                log.debug("New URL was added to PageUrl table.")
            else:
                log.debug("Known URL loaded from PageUrl table.")
            page_urls = [page_url]
        else:
            query = PageUrl.objects.filter(is_active=True).order_by("-last_polled_on")
            if not all_urls:
                query = query[:1]
            page_urls = query

        for page_url in page_urls:
            log.debug("URL %s", page_url.url)

            html = ndutils.fetch(page_url.url)
            log.debug("Fetched %d Bytes of HTML.", len(html))
            page_text = PageText(url=page_url, html=html)
            page_url.last_polled_on = ndutils.now()

            page_text.text = ndparsers.get_parser(page_url.url)(page_text.html)
            page_url.last_parsed_on = ndutils.now()
            log.debug("Parsed into %d Bytes of text.", len(page_text.text))

            page_text.save()
            page_url.save()
