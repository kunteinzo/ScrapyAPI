from websockets.sync.client import connect

if __name__ == '__main__':
    with connect('ws://localhost:8000/ws/test') as ws:
        while msg := ws.recv():
            ws.send(input('Msg: '))
            print(msg)