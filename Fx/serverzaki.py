import os
from socket import create_server

SERVER_ENDPOINT = ('', 7500)
BUFFER = 4096

with create_server(SERVER_ENDPOINT) as ss:
    print("Server bound to Port", SERVER_ENDPOINT[1])
    while True:
        print("Server listening...")
        conn, client_endpoint = ss.accept()
        with conn:
            header = conn.recv(1024).decode().strip()
            parts = header.split()
            command = parts[0].lower()

            if command == "download":
                filename = parts[1]
                if os.path.exists(filename):
                    filesize = os.path.getsize(filename)
                    conn.sendall(f"OK {filesize}\n".encode())
                    with open(filename, "rb") as f:
                        while chunk := f.read(BUFFER):
                            conn.sendall(chunk)
                else:
                    conn.sendall(b"NOT FOUND\n")

            elif command == "upload":
                filename = parts[1]
                filesize = int(parts[2])
                remaining = filesize
                try:
                    with open(filename, "wb") as f:
                        while remaining > 0:
                            chunk = conn.recv(min(BUFFER, remaining))
                            if not chunk:
                                break
                            f.write(chunk)
                            remaining -= len(chunk)
                    if remaining == 0:
                        conn.sendall(b"STORED\n")
                    else:
                        conn.sendall(b"FAILED\n")
                except Exception:
                    conn.sendall(b"FAILED\n")

            else:
                conn.sendall(b"FAILED\n")
