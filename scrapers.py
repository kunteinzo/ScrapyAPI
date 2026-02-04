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
from json import loads
from random import randint
from re import compile, search as rsearch

from bs4 import BeautifulSoup
from requests import get, post

from models import ResponseBlock, WatchBlock, VideoBlock

_url_mahar = 'https://api.maharprod.com/'


def headers():
    """
    Prepare auth header for scraping Mahar
    """
    resp = post(f'{_url_mahar}profile/v1/RefreshToken', headers={'Content-Type': 'application/json'},
                data='{"refreshToken": "AMf-vBwNKNmDEzv4BXB8X2s50f-TLJJG3qpf_UuhaobP8jmtm2wbj5hSf1OgE1vuPia3nV8_D2ksrJ-FyETShA6sciBh2UiOhZxFpPmFZs6SL5jsPsG5ptmVxIKopcFiuUxYXxbVN68N5JuDEqMd68HZH8UY_rtWIvofEq0y4v5eP7GEzVXil0Y"}')
    return {'Authorization': resp.json()['access_token']}


def movies(pn: int):
    resp = get(f'{_url_mahar}display/v1/moviebuilder?pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def series(pn: int):
    resp = get(f'{_url_mahar}display/v1/seriesbuilder?pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def playlist(_id: str, pn: int):
    resp = get(f'{_url_mahar}display/v1/playlistDetail?id={_id}&pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def movie_detail(_id: str):
    resp = get(f'{_url_mahar}content/v1/MovieDetail/{_id}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def movie_stream(_id: str):
    resp = get(
        f'{_url_mahar}revenue/url?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)


def series_detail(_id: str):
    resp = get(f'{_url_mahar}content/v1/SeriesDetail/{_id}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def season(_id: str):
    resp = get(
        f'{_url_mahar}content/v1/Seasons?&filter=seriesId+eq+b1b6cf80-6e1b-4142-bd01-c32a3496f595&select=nameMm%2CnameEn%2Cid',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def episode(_id: str):
    resp = get(
        f'{_url_mahar}content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+0f95491d-2a64-4107-a0d3-776dffdf07a0&orderby=sorting+desc&top=100&skip=0',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def series_stream(_id: str):
    resp = get(
        f'{_url_mahar}revenue/url?type=episodes&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile',
        headers=headers())
    resp.encoding = 'utf-8'
    print(resp.text)
    return loads(resp.text)


def mahar_deep_scrape():
    data = []
    pn = 1
    while len(res := movies(pn)) > 0:
        pn += 1
        for pl in res:
            print(pl['titleEn'])
            pn1 = 1
            while len(pl_res := playlist(pl['playlistId'], pn1)) > 0:
                pn1 += 1
                for mv in pl_res:
                    data.append(mv)

    pn = 1
    while len(res := series(pn)) > 0:
        pn += 1
        for pl in res:
            print(pl['titleEn'])
            pn1 = 1
            while len(pl_res := playlist(pl['playlistId'], pn1)) > 0:
                pn1 += 1
                for se in pl_res:
                    data.append(se)
    return data


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


def get_pagination(soup: BeautifulSoup):
    if pagi := soup.find('div', class_='pagination'):
        if lp := pagi.find('a', class_='last-page'):
            lp = lp.get('href')
            return int(lp[lp.rindex('/') + 1:])
    return None


def get_related(soup: BeautifulSoup):
    if script := soup.find('script', string=compile('video_related=')):
        script = script.text.replace('\\/', '/')
        related = loads(rsearch('\[\{.*}]', script).group())
        return [VideoBlock(
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
        ) for rd in related]
    return None


def get_script_content(script: str):
    hls = thumb = thumb169 = slide = slide_big = slide_minute = None
    if _hls := rsearch(r'VideoHLS.*\'', script):
        hls = _hls.group()
        hls = hls[len('VideoHLS(\''):len(hls) - 1]
    if _thumb := rsearch(r'ThumbUrl.*\'', script):
        thumb = _thumb.group()
        thumb = thumb[len('ThumbUrl(\''):len(thumb) - 1]
    if _thumb169 := rsearch(r'ThumbUrl169.*\'', script):
        thumb169 = _thumb169.group()
        thumb169 = thumb169[len('ThumbUrl169(\''): len(thumb169) - 1]
    if _slide_minute := rsearch(r'ThumbSlideMinute.*\'', script):
        slide_minute = _slide_minute.group()
        slide_minute = slide_minute[len('ThumbSlideMinute(\''):len(slide_minute) - 1]
    if _slide_big := rsearch(r'ThumbSlideBig.*\'', script):
        slide_big = _slide_big.group()
        slide_big = slide_big[len('ThumbSlideBig(\''):len(slide_big) - 1]
    if _slide := rsearch(r'ThumbSlide.*\'', script):
        slide = _slide.group()
        slide = slide[len('ThumbSlide(\''):len(slide) - 1]
    return hls, thumb, thumb169, slide, slide_big, slide_minute


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
