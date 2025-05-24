def register_webrtc_events(sio):
    @sio.event
    async def join_room(sid, data):
        room = data.get("room")
        await sio.enter_room(sid, room)
        print(f"{sid} joined room {room}")

    @sio.event
    async def offer(sid, data):
        await sio.emit('offer', data, room=data["to"])


    @sio.event
    async def answer(sid, data):
        await sio.emit('answer', data, row=data["to"])


    @sio.event
    async def ice_candidate(sid, data):
        await sio.emit('ice_candidate', data, room=data["to"])