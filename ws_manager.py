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

from fastapi import WebSocket
from random import randint
from uuid import uuid4

class Wsu():
    
    def __init__(self, ws: WebSocket):
        self.uid = str(uuid4())
        self.ws = ws


class WSM():
    
    
    def __init__(self):
        self.active : list[Wsu] = []
    
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        wsu = Wsu(ws)
        self.active.append(wsu)
        return wsu.uid
    
    
    def disconnect(self, ws: WebSocket):
        if wsu := next((u for u in self.active if u.ws == ws), None):
            self.active.remove(wsu)
    
    
    async def send(self, ws: WebSocket, msg: str):
        await ws.send_text(msg)
    
    
    async def broadcast(self, msg: str):
        for ac in self.active:
            await ac.ws.send_text(msg)