from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./templates/")

websockets = [] 
messages = []

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def broadcast(message: str):
    for websocket in app.websockets:
        await websocket.send_text(message)

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    try:
        app.websockets.add(websocket)

        for message in messages:
            await websocket.send_text(message)

        while True:
            data = await websocket.receive_text()
            messages.append(data)

            await broadcast(data)

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        app.websockets.remove(websocket)