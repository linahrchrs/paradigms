from socket import create_connection
import argparse

SERVER_ENDPOINT = ("localhost", 7500)
BUFFER = 4096

parser = argparse.ArgumentParser(description="Log Analysis Client")
parser.add_argument("command", type=str)
parser.add_argument("filename", type=str)
args = parser.parse_args()

with create_connection(SERVER_ENDPOINT) as socket:
    # Send request header
    header = f"{args.command} {args.filename}\n"
    socket.sendall(header.encode())

    # Receive response
    if args.command == "COUNT":
        response = socket.recv(BUFFER).decode().strip()
        parts = response.split()
        
        if parts[0] == "OK":
            print(f"Total requests: {parts[1]}")
        else:
            print("File not found on server")

    elif args.command == "STATUS":
        response = b""
        while True:
            chunk = socket.recv(BUFFER)
            if not chunk:
                break
            response += chunk
        
        lines = response.decode().strip().split('\n')
        if lines[0].startswith("NOT"):
            print("File not found on server")
        else:
            print("Status Code Distribution:")
            for line in lines:
                parts = line.split()
                if parts[0] == "OK":
                    print(f"  {parts[1]}: {parts[2]} occurrences")
    else: 
        msg = socket.recv(1024).decode().strip()
        print(msg)

