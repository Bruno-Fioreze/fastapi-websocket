from typing import List

from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./templates/")

websockets = [] 
messages = []

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    websockets.append(websocket)

    if messages:
        await websocket.send_json(messages)

    while True:
        data = await websocket.receive_text()
        message = f"Message text was: {data}"
        messages.append(message)

        for ws in websockets:
            await ws.send_text(message)