import asyncio  # imports the module asyncio which is in the TPSL ( The Python Standard Libary )

import aioconsole

print("-- SERVER --")  # this is so we know which one is the server console

client_manager = {}


def get_key(address):
    return f"CLIENT__{len(client_manager)}__{address[0]}_{address[1]}"


class MyServer(asyncio.Protocol):
    def __init__(self):
        self.address = None
        self.transport = None
        self.key = None

        # FOR INPUT - comment when use in production
        asyncio.create_task(self.send_data())

    def connection_made(self, transport):
        # transport.get_extra_info("peername") returns a list which has two index IP = [0] and PORT [1]
        self.address = transport.get_extra_info("peername")
        self.transport = transport
        self.key = get_key(self.address)

        print(f"\nNew comming client: {self.address}")
        # manage all client
        client_manager[self.key] = transport

        # Send info to client
        transport.write(f"==> Recieved a connect from {str(self.address)}".encode())

    def connection_lost(self, exception):
        # Show ip client info here
        print(f"\nConnection Lost Client: {self.address}")

        # remove lost client
        del client_manager[self.key]

        if not (exception is None):
            print(f"Reason For Disconection: {exception}")

    def data_received(self, data):
        try:
            recived_data = data.decode()
            print(f"-- Recieved data from client {self.address}::: {recived_data}")
        except Exception as e:
            print(f"An Exception Was Caught In DATA_RECEIVED: {e}")

    async def send_data(self):
        while True:
            try:
                inp_message = await aioconsole.ainput('Input to send to client: ')

                # Send to all client in client manager
                for key in client_manager:
                    print(f"+++ Send data to {str(self.address)}")
                    client_manager[key].write(str(inp_message).encode())

            except Exception as e:
                print(f"An Exception Was Caught In SEND_DATA: {e}")
                break


async def main(host, port):
    try:
        loop = asyncio.get_running_loop()
        my_server = await loop.create_server(MyServer, host, port)
        await my_server.serve_forever()
    except Exception as e:
        print(f"Exception from running server: {e}")


asyncio.run(main("127.0.0.1", 42069))
