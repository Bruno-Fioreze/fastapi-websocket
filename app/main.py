from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./templates/")

websockets = [] 

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    websockets.append(websocket)

    while True:
        data = await websocket.receive_text()
        for ws in websockets:
            await ws.send_text(f"Message text was: {data}")
