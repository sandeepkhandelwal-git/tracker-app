import socketio
import asyncio

sio = socketio.AsyncClient(logger=True)

@sio.event
async def connect():
    print('✅ Connected to server')

@sio.event
async def connect_error(data):
    print('❌ Failed to connect to server:', data)

@sio.event
async def disconnect():
    print('🔌 Disconnected from server')

async def main():
    try:
        await sio.connect('http://localhost:8000', transports=['websocket'])
        await sio.emit('update_location', {
            'user_id': 1,
            'latitude': 12.9716,
            'longitude': 77.5946
        })
        await asyncio.sleep(1)  # Wait for server to process
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        await sio.disconnect()

asyncio.run(main())
