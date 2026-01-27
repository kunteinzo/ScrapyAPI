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

from typing import Annotated
from json import loads
from html import unescape

from fastapi import APIRouter, Query, Path
from requests import get
from bs4 import BeautifulSoup
from re import compile, search as rsearch

from models import ResponseBlock, VideoBlock, WatchBlock

router = APIRouter(prefix='/xvideos', tags=['Xvideos'])


def xvideos(
        page: int = 0,
        search: str|None = None,
        watch: str|None = None
):
    url = 'https://www.xvideos.com'
    
    if search:
        url += f'/?k={search}{f"&p={page}" if page > 0 else ""}'
    elif watch:
        url += watch+'#show-related'
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
            stream = rsearch(r'VideoHLS.*\'', script).group()
            thumb = rsearch(r'ThumbUrl.*\'', script).group()
            thumb169 = rsearch(r'ThumbUrl169.*\'', script).group()
            slide_minute = rsearch(r'ThumbSlideMinute.*\'', script).group()
            slide_big = rsearch(r'ThumbSlideBig.*\'', script).group()
            slide = rsearch(r'ThumbSlide.*\'', script).group()
            
            wb.title = wb.description = unescape(title[len('VideoTitle(\''):len(title)-1])
            
            wb.hls = stream[len('VideoHLS(\''):len(stream) - 1]
            wb.thumb = thumb[len('ThumbUrl(\''):len(thumb) - 1]
            wb.thumb169 = thumb169[len('ThumbUrl169(\''): len(thumb169) - 1]
            wb.slide = slide[len('ThumbSlide(\''):len(slide) - 1]
            wb.slide_big = slide_big[len('ThumbSlideBig(\''):len(slide_big) - 1]
            wb.slide_minute = slide_minute[len('ThumbSlideMinute(\''):len(slide_minute) - 1]
        
        if script := soup.find('script', string=compile('video_related=')):
            script = script.text.replace('\\/', '/')
            rela = loads(rsearch('\[\{.*}]', script).group())
            
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

            wb.related = [VideoBlock(
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
        return wb
    
    xr = ResponseBlock()
    if pagi := soup.find('div', class_='pagination'):
        if lp := pagi.find('a', class_='last-page'):
            lp = lp.get('href')
            xr.pages = int(lp[lp.rindex('/')+1:])
    for bl in soup.find_all('div', class_='thumb-block'):
        xb = VideoBlock()
        if title := bl.find('a', title=compile('.')):
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
        xr.content.append(xb)
    return xr


@router.get('/main')
def xvideos_main(
        page: Annotated[int, Query()] = 0
) -> ResponseBlock:
    return xvideos(page)


@router.get('/search/{search}')
def xvideos_search(
        search: Annotated[str, Path()],
        page: Annotated[int, Query()] = 0
) -> ResponseBlock:
    return xvideos(page, search)


@router.get('/watch')
def xvideos_watch(link: Annotated[str, Query()]) -> WatchBlock:
    return xvideos(watch=link)