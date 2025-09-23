from socket import create_connection

SERVER_ENDPOINT = ('localhost', 7777)

with create_connection(SERVER_ENDPOINT) as socket:
    message = socket.recv(20).decode()
    print(message)