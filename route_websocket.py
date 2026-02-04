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

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from ws_manager import WSM

router = APIRouter(prefix='/ws', tags=['WebSocket'])

wsm = WSM()

@router.websocket('/test')
async def ws_route(ws: WebSocket):
    token = ws.headers.get('authorization')
    
    if not token and not token.startswith('Bearer '):
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    if token[7:] != 'yes':
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    uid = await wsm.connect(ws)
    
    try:
        while True:
            data = await ws.receive_json()
            if data['type'] == 'gp':
                await wsm.broadcast(data["msg"])
    except WebSocketDisconnect as e:
        wsm.disconnect(ws)
        await wsm.broadcast(f'User {uid} has left the group')
