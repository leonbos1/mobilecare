import asyncio
import websockets

async def echo(websocket, path):

    async for message in websocket:
        if path.replace('/', '') == '2':
            await websocket.send(f'{message}')
            await websocket.send(f'data van de server')


start_server = websockets.serve(echo, '127.0.0.1', 4000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

