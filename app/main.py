# app/main.py

import socketio as socio
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.events import location
from app.socket_handlers.webrtc import register_webrtc_events
#create an async socket.io server
sio = socio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

#create fastapi app
fastapi_app = FastAPI()
fastapi_app.mount('/static/',StaticFiles(directory="app/static"),name="static")

#Route to serve the HTML file directly
@fastapi_app.get("/walkie")
async def get_walkie_page():
    file_path = os.path.join("app", "static", "html", "webrtc_client.html")
    return FileResponse(file_path)
#mount the socket.io server onto fastapi
app = socio.ASGIApp(sio,other_asgi_app=fastapi_app)

#register event handlers
location.register_location_events(sio)

#register webrtc event
register_webrtc_events(sio)