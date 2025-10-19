import os
from socket import create_server

SERVER_ENDPOINT = ('', 7500)
BUFFER = 4096

def count_requests(filename):
    """Count total number of requests in CLF log file"""
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():  # Count non-empty lines
                count += 1
    return count

def status_distribution(filename):
    """Get distribution of HTTP status codes"""
    status_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                # CLF format: status code is typically the 9th field (0-indexed: 8)
                parts = line.split()
                if len(parts) >= 9:
                    status = parts[8]
                    status_dict[status] = status_dict.get(status, 0) + 1
    return status_dict

with create_server(SERVER_ENDPOINT) as ss:
    print(f"Server bound to Port {SERVER_ENDPOINT[1]}")
    while True:
        print("Server listening...")
        socket, client_endpoint = ss.accept()
        with socket:
            header = socket.recv(1024).decode().strip()
            parts = header.split()
            command = parts[0].upper()
            filename = parts[1] if len(parts) > 1 else ""

            if command == "COUNT":
                if os.path.exists(filename):
                    try:
                        total = count_requests(filename)
                        socket.sendall(f"OK {total}\n".encode())
                    except Exception as e:
                        socket.sendall(b"NOT FOUND\n")
                else:
                    socket.sendall(b"NOT FOUND\n")

            elif command == "STATUS":
                if os.path.exists(filename):
                    try:
                        status_dict = status_distribution(filename)
                        for status, count in status_dict.items():
                            socket.sendall(f"OK {status} {count}\n".encode())
                    except Exception as e:
                        socket.sendall(b"NOT FOUND\n")
                else:
                    socket.sendall(b"NOT FOUND\n")

            else:
                socket.sendall(b"INVALID COMMAND\n")

