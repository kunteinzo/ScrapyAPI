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

from pydantic import BaseModel


class VideoBlock(BaseModel):
    title: str | None = None
    link: str | None = None
    mk_name: str | None = None
    mk_link: str | None = None
    thumb: str | None = None
    thumb_sfw: str | None = None
    thumb_mzl: str | None = None
    pvv: str | None = None
    duration: str | None = None
    resolution: str | None = None


class ResponseBlock(BaseModel):
    pages: int = 0
    content: list[VideoBlock] = []


class WatchBlock(BaseModel):
    title: str | None = None
    description: str | None = None
    mk_name: str | None = None
    mk_link: str | None = None
    hls: str | None = None
    thumb: str | None = None
    thumb169: str | None = None
    slide: str | None = None
    slide_big: str | None = None
    slide_minute: str | None = None
    related: list[VideoBlock] = []
