from socket import create_connection
import argparse

SERVER_ENDPOINT=('localhost', 8000)

parser = argparse.ArgumentParser()
parser.add_argument ("command", type=str)
parser.add_argument ("filename", type = str)
args = parser.parse_args()

with create_connection(SERVER_ENDPOINT) as socket:
    file_name = args.filename

    if args.command == "SIZE":
        header = f"SIZE {file_name}\n"
        socket.sendall(header.encode())
        response = socket.recv(1024).decode().strip()
        token, *rest = response.split(" ")
        if token != "NOT":
            file_size = int(rest[0])
            print("size:", file_size)
        else:
            print("Error: File Not Found!\n")
    
    elif args.command == "TYPE":
        header = f"TYPE {file_name}\n"
        socket.sendall(header.encode())
        response = socket.recv(1024).decode().strip()
        token, *rest = response.split(" ")
        if token != "NOT":
            file_type = str(rest[0])
            print("type:", file_type)
        else:
            print("Error: File Not Found!\n")
    
    else:
        print("Wrong command\n")