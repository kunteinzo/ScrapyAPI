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
        xv = VideoBlock()
        if title := soup.find('div', class_='video-title'):
            xv.title = title.find('strong').text.strip()
        if desc := soup.find('p', class_='video-description'):
            xv.description = desc.text.strip()
        if mk := soup.find('a', class_='free-plate'):
            xv.mk_name = mk.text.strip()
            xv.mk_link = mk.get('href')
        if script := soup.find('script', string=compile('video_related=')):
            script = script.text
            rela = loads(rsearch(r'\[\{.*}]', script).group().replace('\\/', '/'))

            def get_resolution(r):
                if r.get('fk') == 1:
                    return '4K'
                if r.get('td') == 1:
                    return '1440p'
                if r.get('hp') == 1:
                    return '1080p'
                if r.get('h') == 1:
                    return '720p'
                if r.get('hm') == 1:
                    return '480p'
                else:
                    return '360p'

            xv.related = [VideoBlock(
                title=rd.get('t'),
                link=rd.get('u'),
                thumb=rd.get('i'),
                thumb_sfw=rd.get('st1'),
                thumb_mzl=rd.get('mu'),
                pvv=rd.get('ipu'),
                mk_name=rd.get('pn'),
                mk_link=rd.get('pu'),
                duration=rd.get('d'),
                resolution=get_resolution(rd)
            ) for rd in rela]
        if script := soup.find('script', crossorigin='anonymous', string=compile('html5player')).text:
            stream = rsearch(r'VideoHLS.*\'', script).group()
            thumb = rsearch(r'ThumbUrl.*\'', script).group()
            thumb169 = rsearch(r'ThumbUrl169.*\'', script).group()
            slide_minute = rsearch(r'ThumbSlideMinute.*\'', script).group()
            slide_big = rsearch(r'ThumbSlideBig.*\'', script).group()
            slide = rsearch(r'ThumbSlide.*\'', script).group()
            xv.hls = stream[len('VideoHLS(\''):len(stream) - 1]
            xv.thumb = thumb[len('ThumbUrl(\''):len(thumb) - 1]
            xv.thumb169 = thumb169[len('ThumbUrl169(\''): len(thumb169) - 1]
            xv.slide = slide[len('ThumbSlide(\''):len(slide) - 1]
            xv.slide_big = slide_big[len('ThumbSlideBig(\''):len(slide_big) - 1]
            xv.slide_minute = slide_minute[len('ThumbSlideMinute(\''):len(slide_minute) - 1]
        return xv

    xnxx_response = ResponseBlock()

    if pagi := soup.find('div', class_='pagination'):
        if lastpage := pagi.find('a', class_='last-page'):
            lp = lastpage.get('href')
            xnxx_response.pages = int(lp[lp.rindex('/') + 1:])

    for tb in soup.find_all('div', class_='thumb-block'):
        _id = tb['data-id']
        xb = VideoBlock()

        if title := tb.find('a', title=compile('.')):
            xb.title = title.get('title')
            xb.link = title.get('href')

        if mk := tb.find('a', href=compile('/porn-maker/')):
            xb.mk_name = mk.text.strip()
            xb.mk_link = mk.get('href')

        if img := tb.find('img', id=f'pic_{_id}'):
            xb.thumb = img.get('data-src')
            xb.thumb_sfw = img.get('data-sfwthumb')
            xb.thumb_mzl = img.get('data-mzl')
            xb.pvv = img.get('data-pvv')

        if me := tb.find('p', class_='metadata'):
            if duration := rsearch(r'\d+(min|sec)', me.text):
                xb.duration = duration.group()
            if rating := rsearch(r'\d+%', me.text):
                xb.rating = rating.group()
            if watched := rsearch(r'[\d.]+(B|M|k)?', me.text):
                xb.watched = watched.group()
            if resolution := rsearch(r'\d+(K|p)', me.text):
                xb.resolution = resolution.group()

        xnxx_response.content.append(xb)
    return xnxx_response


@router.get("/search/{search}")
def xnxx_search(
        search: Annotated[str, Path()],
        page: Annotated[int, Query()] = 0
) -> ResponseBlock:
    return xnxx(search=search, page=page, mode=mode, period=period, length=length, quality=quality)


@router.get("/best")
def xnxx_best(
        year: Annotated[int, Query(ge=1999, le=2026)],
        month: Annotated[int, Query(ge=1, le=12)],
        page: Annotated[int, Query()] = 0
) -> ResponseBlock:
    return xnxx(year=year, month=month, page=page)


@router.get("/watch")
def xnxx_watch(
        link: Annotated[str, Query()]
) -> WatchBlock:
    return xnxx(watch=link)
