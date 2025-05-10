import socketio
import asyncio
import random

#SERVER_URL = 'http://localhost:8000'
SERVER_URL = 'http://37.59.30.197'
NUM_CLIENTS = 2

# Generate random latitude/longitude around a central point
def generate_random_location():
    base_lat = 12.9716  # Bengaluru center
    base_lon = 77.5946
    return (
        base_lat + random.uniform(-0.01, 0.01),
        base_lon + random.uniform(-0.01, 0.01)
    )

async def simulate_client(user_id: int):
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print(f'✅ [User {user_id}] Connected')

        # Send initial location
        latitude, longitude = generate_random_location()
        await sio.emit('update_location', {
            'user_id': user_id,
            'latitude': latitude,
            'longitude': longitude
        })

    @sio.event
    async def disconnect():
        print(f'🔌 [User {user_id}] Disconnected')

    @sio.on('user_location_update')
    async def on_user_location_update(data):
        if data['user_id'] != user_id:
            print(f'📍 [User {user_id}] Received location of User {data["user_id"]}: '
                  f'({data["latitude"]}, {data["longitude"]})')

    try:
        await sio.connect(SERVER_URL, transports=['websocket'])
        await asyncio.sleep(10)  # Keep the client active to listen for others
    except Exception as e:
        print(f'❌ [User {user_id}] Error: {e}')
    finally:
        await sio.disconnect()

async def main():
    tasks = [simulate_client(user_id) for user_id in range(1, NUM_CLIENTS + 1)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())