"""
ScrapyAPI scrape some stuff.

Copyright (C) 2026  Kanye Sue

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from html import unescape
from re import compile, search as rsearch
from typing import Annotated

from bs4 import BeautifulSoup
from fastapi import APIRouter, Query, Path
from requests import get

from models import ResponseBlock, VideoBlock, WatchBlock
from utils import get_pagination, get_related, get_script_content

router = APIRouter(prefix='/xvideos', tags=['Xvideos'])


def xvideos(
        page: int = 0,
        search: str | None = None,
        watch: str | None = None
):
    url = 'https://www.xvideos.com'

    if search:
        url += f'/?k={search}{f"&p={page}" if page > 0 else ""}'
    elif watch:
        url += watch + '#show-related'
    elif page > 0:
        url += f'/new/{page}'

    soup = BeautifulSoup(get(url).content, 'html.parser')

    if watch:
        wb = WatchBlock()
        if uploader := soup.find('a', class_='uploader-tag'):
            wb.mk_link = uploader.get('href')
            wb.mk_name = uploader.text.strip()
        if script := soup.find('script', string=compile('VideoHLS')):
            script = script.text
            title = rsearch(r'VideoTitle.*\'', script).group()
            wb.title = wb.description = unescape(title[len('VideoTitle(\''):len(title) - 1])
            wb.hls, wb.thumb, wb.thumb169, wb.slide, wb.slide_big, wb.slide_minute = get_script_content(script)

        wb.related = get_related(soup)
        return wb

    rb = ResponseBlock()

    rb.pages = get_pagination(soup)

    for bl in soup.find_all('div', class_='thumb-block'):
        xb = VideoBlock()
        if title := bl.find('a', title=compile('')):
            xb.title = title.get('title')
            xb.link = title.get('href')
        if img := bl.find('img', id=f'pic_{bl["data-id"]}'):
            xb.thumb = img.get('data-src')
            xb.thumb_sfw = img.get('data-sfwthumb')
            xb.thumb_mzl = img.get('data-mzl')
            xb.pvv = img.get('data-pvv')
        if name := bl.find('span', class_='name'):
            xb.mk_link = name.parent.get('href')
            xb.mk_name = name.text.strip()
        if resolution := bl.find('span', class_=compile('video-.+-mark')):
            # NOTE: Xvideos Resolution Tag could be null. IDK. They just null.
            xb.resolution = resolution.text.strip()
        if duration := bl.find('span', class_='duration'):
            xb.duration = duration.text.strip()
        rb.content.append(xb)
    return rb


@router.get('/main')
def xvideos_main(
        page: Annotated[int, Query(alias='p', title='Page', description='Page')] = 0
) -> ResponseBlock:
    return xvideos(page)


@router.get('/search/{search}')
def xvideos_search(
        search: Annotated[str, Path()],
        page: Annotated[int, Query(alias='p', title='Page', description='Page')] = 0
) -> ResponseBlock:
    return xvideos(page, search)


@router.get('/watch')
def xvideos_watch(link: Annotated[str, Query()]) -> WatchBlock:
    return xvideos(watch=link)
