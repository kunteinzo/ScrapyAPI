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

from fastapi import APIRouter, Path, Query

from models import ResponseBlock, WatchBlock
from scrapers import xnxx

router = APIRouter(prefix='/xnxx', tags=['Xnxx'])


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
