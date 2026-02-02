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

from requests import get, post

_domain = 'https://api.maharprod.com/'


def headers():
    resp = post(f'{_domain}profile/v1/RefreshToken', headers={'Content-Type': 'application/json'},
                data='{"refreshToken": "AMf-vBwNKNmDEzv4BXB8X2s50f-TLJJG3qpf_UuhaobP8jmtm2wbj5hSf1OgE1vuPia3nV8_D2ksrJ-FyETShA6sciBh2UiOhZxFpPmFZs6SL5jsPsG5ptmVxIKopcFiuUxYXxbVN68N5JuDEqMd68HZH8UY_rtWIvofEq0y4v5eP7GEzVXil0Y"}')
    return {'Authorization': resp.json()['access_token']}


def movies(pn: int):
    resp = get(f'{_domain}display/v1/moviebuilder?pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def series(pn: int):
    resp = get(f'{_domain}display/v1/seriesbuilder?pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def playlist(_id: str, pn: int):
    resp = get(f'{_domain}display/v1/playlistDetail?id={_id}&pageNumber={pn}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def movie_detail(_id: str):
    resp = get(f'{_domain}content/v1/MovieDetail/{_id}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def movie_stream(_id: str):
    resp = get(
        f'{_domain}revenue/url?type=movie&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)


def series_detail(_id: str):
    resp = get(f'{_domain}content/v1/SeriesDetail/{_id}', headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def season(_id: str):
    resp = get(
        f'{_domain}content/v1/Seasons?&filter=seriesId+eq+b1b6cf80-6e1b-4142-bd01-c32a3496f595&select=nameMm%2CnameEn%2Cid',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def episode(_id: str):
    resp = get(
        f'{_domain}content/v1/Episodes?&filter=status+eq+true+and+seasonId+eq+0f95491d-2a64-4107-a0d3-776dffdf07a0&orderby=sorting+desc&top=100&skip=0',
        headers=headers())
    resp.encoding = 'utf-8'
    return loads(resp.text)['value']


def series_stream(_id: str):
    resp = get(
        f'{_domain}revenue/url?type=episodes&contentId={_id}&isPremiumUser=true&isPremiumContent=true&source=mobile',
        headers=headers())
    resp.encoding = 'utf-8'
    print(resp.text)
    return loads(resp.text)


def mroot():
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
