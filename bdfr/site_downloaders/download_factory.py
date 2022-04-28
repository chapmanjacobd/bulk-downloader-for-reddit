#!/usr/bin/env python3
# coding=utf-8

import re
import urllib.parse
from typing import Type

from bdfr.exceptions import NotADownloadableLinkError
from bdfr.site_downloaders.base_downloader import BaseDownloader
from bdfr.site_downloaders.direct import Direct
from bdfr.site_downloaders.erome import Erome
from bdfr.site_downloaders.fallback_downloaders.ytdlp_fallback import YtdlpFallback
from bdfr.site_downloaders.gallery import Gallery
from bdfr.site_downloaders.gfycat import Gfycat
from bdfr.site_downloaders.imgur import Imgur
from bdfr.site_downloaders.pornhub import PornHub
from bdfr.site_downloaders.redgifs import Redgifs
from bdfr.site_downloaders.self_post import SelfPost
from bdfr.site_downloaders.vidble import Vidble
from bdfr.site_downloaders.youtube import Youtube


class DownloadFactory:
    @staticmethod
    def pull_lever(url: str) -> Type[BaseDownloader]:
        sanitised_url = DownloadFactory.sanitise_url(url)
        if re.match(r".*/.*\.\w{3,4}(\?[\w;&=]*)?$", sanitised_url) and not DownloadFactory.is_web_resource(
            sanitised_url
        ):
            # return Direct
            print(url)
            raise NotADownloadableLinkError()
        elif re.match(r"reddit\.com/r/", sanitised_url):
            return SelfPost
        else:
            print(url)
            raise NotADownloadableLinkError()

    @staticmethod
    def sanitise_url(url: str) -> str:
        beginning_regex = re.compile(r"\s*(www\.?)?")
        split_url = urllib.parse.urlsplit(url)
        split_url = split_url.netloc + split_url.path
        split_url = re.sub(beginning_regex, "", split_url)
        return split_url

    @staticmethod
    def is_web_resource(url: str) -> bool:
        web_extensions = (
            "asp",
            "aspx",
            "cfm",
            "cfml",
            "css",
            "htm",
            "html",
            "js",
            "php",
            "php3",
            "xhtml",
        )
        if re.match(rf'(?i).*/.*\.({"|".join(web_extensions)})$', url):
            return True
        else:
            return False
