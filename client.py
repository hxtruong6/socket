import \
    socket  # the client side doesnt use the asyncio module it only needs the socket module which is in The Python Standard Libary
import time


def send_message(command_of_client="CLIENT_REQUEST", message="Client call serve? Do server hear me?"):
    # convert to string or binary here
    return {
        "start_connection": command_of_client,  # init function
        "some_info": str(message)
    }


print(" -- CLIENT -- ")  # this is so we know which one is the client console


class Server:
    # takes the server ip and port
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((self.host_ip, self.host_port))  # connects to the hosts ip and port
            self.sock.settimeout(1)  # sets timeout to 1 second
        except:
            pass

    def send_data(self, data):
        self.sock.send(str(data).encode())  # turns string into utf-8

    def close_connection(self):  # closes connection
        self.sock.close()

    def receive_data(self):
        buffer_size = 256  # the buffer size
        data = b''  # makes sure the data is in bytes
        while True:
            try:
                chunk = self.sock.recv(buffer_size)  # sends it to the socket in chunks as this is how TCP works
            except:
                break
            data += chunk  # adds it to the string of bytes each loop
            if len(chunk) == 0:
                break
        # print(f"Recie: {data}")
        return data
        # try:
        #     text_dict = ast.literal_eval(data.decode())  # uses ast.literal_eval to check if its a python datatype
        #     return text_dict
        # except:
        #     return None

    def is_connected(
            self):  # checks if there is a connection by sending a small packet and if it is sent successfully then return true else return false
        try:
            self.sock.send("".encode())
            return True
        except:
            return False


# sever constructor
s = Server("127.0.0.1", 42069)  # setting the ip and port of the server we are trying to connect to


def handleClientSendData(client_socket, command_of_client, message):
    # client_socket.send_data(send_message(command_of_client=command_of_client, message=message))
    data = client_socket.receive_data()  # getting everything recived an storing it in an varible
    # if no data recived then tell the client that there was none then close the program
    if data is None:
        print("No Data Recived :(")
    else:
        print(f"Data from server: {data}\n")
        # for key, value in data.items():
        #     print("".join(value))


if s.is_connected():
    # sending our requests which is to call the starting function on the server (the initiation function )
    handleClientSendData(s, command_of_client="REQUEST_CONNECT", message="Goi den de connect ne.")
    while True:
        # checking if the try is less than or equal to the amount of times we want to try
        # if it connects successfully
        if s.is_connected():
            # pauses the connection - doi client gui data len
            # input_message = input("Nhap data muon gui len server: ")
            input_message = f"Gui den server nef: REQUEST_AT_{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
            handleClientSendData(
                s,
                command_of_client=f"REQUEST_AT_{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}",
                message=input_message
            )
            time.sleep(2)
        else:
            s.close_connection()
            print("Currently Unconnectable :/")  # This means the client was refused or the server script is not running
            quit()
else:
    print("Failed To Connect")
    quit()
