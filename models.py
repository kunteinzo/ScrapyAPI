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
