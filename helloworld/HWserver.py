from socket import create_server

SERVER_ENDPOINT = ('', 7777)

with create_server (SERVER_ENDPOINT) as ss:
    print("Server bound to port: ", SERVER_ENDPOINT[1])
    while True:
        print ("Server listening...")
        (socket, client_endpoint) = ss .accept ()
        with socket:
            print(f'Connected from {client_endpoint}')
            socket.send('Hello World!'.encode())