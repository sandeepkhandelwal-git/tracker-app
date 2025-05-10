#app/events/location.py
from app.database.session import SessionLocal
from app.database.location_store import save_user_location

def register_location_events(sio):
    @sio.event
    async def connect(sid, environ):
        print(f"Client Connected: {sid}")

    @sio.event
    async def disconnect(sid):
        print(f"Client Disconnected: {sid}")

    @sio.event
    async def update_location(sid, data):
        """
        Handle incoming location updates.
        Expected 'data' format:
        {
        "user_id" : "user123",
        "latitude" : 12.9716,
        "longitude" : 77.5946
        }
        """
        print(f"Received location from {sid}:{data}")

        db =SessionLocal()
        try:
            save_user_location(db,
                               data["user_id"],
                               data["latitude"],
                               data["longitude"])

            #create location payload
            location_payload ={
                "user_id": data["user_id"],
                "latitude": data["latitude"],
                "longitude": data["longitude"]
            }
            #emit the success acknowledgement
            await sio.emit('location_updated',
                           {
                               **location_payload,
                               "status": "received"
                           }
                           ,to=sid)

            #Broadcast to all other connected users except this
            await sio.emit('user_location_update',
                           location_payload,skip_sid=sid)

        except Exception as ex:
            print(f"Error while saving {data["user_id"]} location to database, details are :{ex}")
            await sio.emit('location_updated',
                           {
                               "status" :"error",
                               "error_details" : str(ex)
                           },
                           to=sid
                           )
        finally:
            db.close()
