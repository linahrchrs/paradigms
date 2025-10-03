
from socket import create_server

SERVER_ENDPOINT = ('', 8000)
BUFFER = 4096


with create_server(SERVER_ENDPOINT) as ss:
    print("Server bound to port", SERVER_ENDPOINT[1])
    while True:
        print("server is listening...")
        socket, client_endpoint = ss.accept()
        with socket:
            header = socket.recv(1024).decode().strip()
            parts = header.split()
            operation = parts[0].upper()
            value1 = int(parts[1])
            value2 = int(parts[2])

            if operation == "ADD":
                result = value1 + value2
            elif operation == "SUB":
                result = value1 - value2
            elif operation == "MUL":
                result = value1 * value2
            elif operation == "DIV":
                if value2 == 0:
                    result = f"ERROR"
                else: 
                    result = value1/value2
            else:
                result = f"ERROR"
            
            socket.sendall(f"{result}\n".encode())
