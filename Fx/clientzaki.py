from socket import create_connection
import argparse
import sys

SERVER_ENDPOINT = ("localhost", 7500)
BUFFER = 4096

parser = argparse.ArgumentParser()
parser.add_argument("function", type=str)
parser.add_argument("filename", type=str)
parser.add_argument("filesize", type=int, nargs='?')
args = parser.parse_args()


with create_connection(SERVER_ENDPOINT) as socket:

    file_name = args.filename

    if args.function == "upload":
        file_size = args.filesize
        with open(file_name, "rb") as file:
            file_bytes = file.read()
        header = f"upload {file_name} {file_size}\n"
        socket.sendall(header.encode())
        socket.sendall(file_bytes)
        msg = socket.recv(1024).decode().strip()
        print(msg)

    
    elif args.function == "download":
        header = f"{args.function} {args.filename}\n".encode() 
        socket.send(header)

        msg = socket.recv(1024).decode().strip()
        token, *rest = msg.split(" ")

        if token != "NOT":
            file_size = int(rest[0])
            file_content = b""
            while len(file_content) < file_size:
                chunk = socket.recv(BUFFER)
                if not chunk:
                    break
                file_content += chunk
                    
            with open(f"download_{file_name}", "wb") as file:
                file.write(file_content)

        else:
            print(msg)
    else:
        print("Wrong Command!")
