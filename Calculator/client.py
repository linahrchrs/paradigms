import argparse
from socket import create_connection

SERVER_ENDPOINT = ('localhost', 8000)
BUFFER = 4096

parser = argparse.ArgumentParser()
parser.add_argument("operation", type=str, choices=["ADD", "SUB", "MUL", "DIV"])
parser.add_argument("value1", type=int)
parser.add_argument("value2", type=int)
args = parser.parse_args()

with create_connection(SERVER_ENDPOINT)  as socket:
    header = f"{args.operation} {args.value1} {args.value2}\n"
    socket.sendall(header.encode())

    msg = socket.recv(1024).decode().strip()
    print(msg)
