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

from json import loads
from random import randint
from re import compile, search as rsearch
from typing import Annotated

from bs4 import BeautifulSoup
from fastapi import APIRouter, Path, Query
from requests import get

from models import ResponseBlock, WatchBlock, VideoBlock
from utils import get_pagination, get_related, get_script_content

router = APIRouter(prefix='/xnxx', tags=['Xnxx'])


def xnxx(
        search: str | None = None,
        page: int = 0,
        watch: str | None = None,
        year: int = 0,
        month: int = 0
):
    url = 'https://www.xnxx.com'

    if search:
        url += f'/search/{search}'
    elif 1999 < year < 2026 and 0 < month < 13:
        url += f'/best/{year}-{month:02d}'
    elif watch:
        url += f'{watch}#show-related'
    else:
        url += '/best'

    if not watch and page > 0:
        url += f'/{page}'

    headers = {}
    with open('ua.json', 'r') as f:
        ua = loads(f.read())
        headers['User-Agent'] = ua[randint(0, len(ua))]

    soup = BeautifulSoup(get(url, headers=headers).content, 'html.parser')

    if watch:
        vb = WatchBlock()
        if title := soup.find('div', class_='video-title'):
            vb.title = title.find('strong').text.strip()
        if desc := soup.find('p', class_='video-description'):
            vb.description = desc.text.strip()
        if mk := soup.find('a', class_='free-plate'):
            vb.mk_name = mk.text.strip()
            vb.mk_link = mk.get('href')
        vb.related = get_related(soup)
        if script := soup.find('script', crossorigin='anonymous', string=compile('html5player')).text:
            vb.hls, vb.thumb, vb.thumb169, vb.slide, vb.slide_big, vb.slide_minute = get_script_content(script.text)
        return vb

    rb = ResponseBlock()

    rb.pages = get_pagination(soup)

    for bl in soup.find_all('div', class_='thumb-block'):

        xb = VideoBlock()

        if title := bl.find('a', title=compile('')):
            xb.title = title.get('title')
            xb.link = title.get('href')

        if mk := bl.find('a', href=compile('/porn-maker/')):
            xb.mk_name = mk.text.strip()
            xb.mk_link = mk.get('href')

        if img := bl.find('img', id=f'pic_{bl['data-id']}'):
            xb.thumb = img.get('data-src')
            xb.thumb_sfw = img.get('data-sfwthumb')
            xb.thumb_mzl = img.get('data-mzl')
            xb.pvv = img.get('data-pvv')

        if me := bl.find('p', class_='metadata'):
            if duration := rsearch(r'\d+(min|sec)', me.text):
                xb.duration = duration.group()
            if resolution := rsearch(r'\d+(K|p)', me.text):
                xb.resolution = resolution.group()

        rb.content.append(xb)
    return rb


@router.get("/best")
def xnxx_best(
        year: Annotated[int, Query(ge=1999, le=2026)] = 2025,
        month: Annotated[int, Query(ge=1, le=12)] = 12,
        page: Annotated[int, Query(alias='p', title='Page', description='Page')] = 0
) -> ResponseBlock:
    return xnxx(year=year, month=month, page=page)


@router.get("/search/{search}")
def xnxx_search(
        search: Annotated[str, Path()],
        page: Annotated[int, Query(alias='p', title='Page', description='Page')] = 0
) -> ResponseBlock:
    return xnxx(search=search, page=page)


@router.get("/watch")
def xnxx_watch(
        link: Annotated[str, Query()]
) -> WatchBlock:
    return xnxx(watch=link)
