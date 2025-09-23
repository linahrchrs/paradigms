import socket
import threading
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 80
SHARE_DIR = "ServerShare"


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        try:
            # Read one line (header)
            header = self.client_socket.recv(1024).decode().strip()
            if not header:
                return

            parts = header.split(" ")
            if len(parts) < 2:
                print("Invalid header from client:", header)
                return

            command, file_name = parts[0], parts[1]

            if command.lower() == "download":
                file_path = os.path.join(SHARE_DIR, file_name)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        data = f.read()
                    header = f"OK {len(data)}\n"
                    self.client_socket.sendall(header.encode())
                    self.client_socket.sendall(data)
                else:
                    self.client_socket.sendall(b"NOT FOUND\n")

            elif command == "upload":
                if len(parts) < 3:
                    self.client_socket.sendall(b"ERROR Missing file size\n")
                    return

                file_name = parts[1]
                file_size = int(parts[2])

                received = b""
                while len(received) < file_size:
                    chunk = self.client_socket.recv(min(4096, file_size - len(received)))
                    if not chunk:
                        break
                    received += chunk

                os.makedirs(SHARE_DIR, exist_ok=True)
                file_path = os.path.join(SHARE_DIR, file_name)
                with open(file_path, "wb") as f:
                    f.write(received)

                self.client_socket.sendall(b"UPLOAD OK\n")

            else:
                print("Connection from incompatible client")

        except Exception as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            self.client_socket.close()


def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server waiting on port {SERVER_PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handler = ClientHandler(client_socket, client_address)
        handler.start()


if __name__ == "__main__":
    main()
