import asyncio

from websockets import connect


async def main():
    try:
        async with connect(
                'ws://localhost/ws/test',
            additional_headers={
                'Authorization': 'Bearer yes'
            }
        ) as ws:
            try:
                for data in await ws.recv():
                    print(data)
                    await ws.send(input('Data: '))
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
