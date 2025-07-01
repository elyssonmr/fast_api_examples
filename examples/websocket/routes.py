from os import path

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/websocket', tags=['Web Socket'])


connected_clients = {}


@router.get('/')
def chat_page():
    with open(
        f'{path.dirname(__file__)}/templates/index.html', encoding='utf-8'
    ) as html_file:
        return HTMLResponse(html_file.read())


@router.websocket_route('/ws_chat')
async def on_message(websocket: WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.receive_json()
        sender = message['sender']
        text = message['message']
        if sender not in connected_clients:
            connected_clients[sender] = websocket

        for client, socket in connected_clients.items():
            if client != sender:
                await socket.send_json({'sender': sender, 'text': text})
