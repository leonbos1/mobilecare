import asyncio
import json

import websockets

connect_users = []

async def echo(websocket, path):
    user = {
        'websocket': websocket,
        'path': path
    }

    if not any(x['path'] == path for x in connect_users):
        connect_users.append(user)
    else:
        for x in connect_users:
            if path == x['path']:
                x['websocket'] = websocket

    async for message in websocket:
        if path.replace('/', '') == 'server':
            obj = json.loads(message)

            for socket in connect_users:
                if socket['path'].replace('/', '') in obj['nurses']:
                    await socket['websocket'].send(f'{obj["patient_name"]}')


start_server = websockets.serve(echo, '127.0.0.1', 4000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


