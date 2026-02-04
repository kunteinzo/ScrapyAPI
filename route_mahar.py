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

from fastapi import APIRouter, Path

from celery_app import celery_app
from tasks import mahar_root

router = APIRouter(prefix='/mahar', tags=['Mahar'])


@router.get('/task/main')
def mahar_main():
    task = mahar_root.delay()
    return dict(task_id=task.id)


@router.get('/task/status/{task_id}')
def mahar_main_task(task_id: Annotated[str, Path()]):
    res = celery_app.AsyncResult(task_id)
    return dict(
        status=res.status,
        result=res.result
    )


@router.get('/task/forget/{task_id}')
def mahar_forget_task(task_id: Annotated[str, Path()]):
    res = celery_app.AsyncResult(task_id)
    if res.ready():
        res.forget()
        return dict(msg='Task deleted')
    return dict(msg='Task not deleted')
