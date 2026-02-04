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

from fastapi import APIRouter, Query, Path

from models import ResponseBlock, WatchBlock
from scrapers import xvideos

router = APIRouter(prefix='/xvideos', tags=['Xvideos'])


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
