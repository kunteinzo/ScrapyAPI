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

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, HTMLResponse

from xnxx import router as xnxx_router
from xvideo import router as xvideos_router

app = FastAPI(
    # debug=True,
    title='ScrapyAPI',
    summary='ScrapyAPI scrape some stuff.',
    description="""## It scrape some stuff.""",
    version="0.0.1",
    servers=[
        dict(url='http://hellohost.tz:8000', description='Dev Server'),
        dict(url='http://127.0.0.1:8000', description='Local Dev Server'),
    ],
    terms_of_service='https://example.com',
    contact=dict(
        name='Kanye Sue',
        url='https://example.com',
        email='kanye4112@gmail.com',
    ),
    license_info=dict(
        name='GPLv3', url='http://hellohost.tz:8000/license'
    )
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://hellohost.tz:8000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


app.include_router(xnxx_router)
app.include_router(xvideos_router)


@app.exception_handler(Exception)
def error(r, e):
    return JSONResponse(
        dict(msg="Something is wrong but IDK"),
        500
    )


@app.get('/license', tags=['License'], response_class=HTMLResponse)
def license_url():
    with open('li_cen_se.html') as f:
        return HTMLResponse(f.read())

