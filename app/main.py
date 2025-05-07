# app/main.py

import socketio as socio
from fastapi import FastAPI
from app.events import location

#create an async socket.io server
sio = socio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

#create fastapi app
fastapi_app = FastAPI()

#mount the socket.io server onto fastapi
app = socio.ASGIApp(sio,other_asgi_app=fastapi_app)

#register event handlers
location.register_location_events(sio)