from datetime import timedelta
from typing import List

from fastapi import Depends, WebSocketDisconnect, WebSocket, APIRouter
from sqlalchemy.orm import Session

from dependencies import get_db, get_connection, get_connection, ConnectionManager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept()
    await websocket.send_text(f"Welcome client : {websocket.client}")
    while True:
        data = await websocket.receive_text()
        print(f"message received : {data} from : {websocket.client}")
        await websocket.send_text(f"Message text was: {data}")

@router.websocket("/connect/{client_id}")
async def connect(websocket: WebSocket, client_id: str, manager: ConnectionManager = Depends(get_connection)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")
    except:
        manager.disconnect(websocket)
