import socket
import os
from threading import Thread

class FxServer:
    def __init__(self, port=8080):
        self.port = port
        
    def start(self):
        # Server: ss = create_server((S_IP, S_PORT))
        ss = socket.create_server(('', self.port))
        
        while True:
            print("Server waiting...")
            # Server: (socket, client_endpoint) = ss.accept()
            client_socket, client_endpoint = ss.accept()
            print(f"Connection from: {client_endpoint}")
            
            # Handle each client in a separate thread
            Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        try:
            client_handler = ClientHandler(client_socket)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Connection closing: socket.close()
            client_socket.close()


class ClientHandler:
    def __init__(self, client_socket):
        self.socket = client_socket
        self.interact()
    
    def interact(self):
        try:
            # I/O: bytes = socket.recv(n_bytes)
            header_bytes = self.socket.recv(1024)
            header = header_bytes.decode('utf-8').strip()
            parts = header.split(' ')
            
            if len(parts) < 2:
                print("Invalid header format")
                return
            
            command = parts[0]
            file_name = parts[1]
            
            if command == "download":
                self.handle_download(file_name)
            elif command == "upload":
                self.handle_upload(file_name, parts)
            else:
                print("Connection got from an incompatible client")
        except Exception as e:
            print(f"Error in interact: {e}")
    
    def handle_download(self, file_name):
        try:
            file_path = os.path.join("ServerShare", file_name)
            
            with open(file_path, 'rb') as file_in:
                file_data = file_in.read()
                file_size = len(file_data)
            
            # Send OK response with file size
            header = f"OK {file_size}\n"
            # I/O: socket.send(bytes)
            self.socket.send(header.encode('utf-8'))
            
            # Send file data
            # I/O: socket.send(bytes)
            self.socket.send(file_data)
            print(f"File sent: {file_name} ({file_size} bytes)")
            
        except FileNotFoundError:
            header = "NOT FOUND\n"
            # I/O: socket.send(bytes)
            self.socket.send(header.encode('utf-8'))
        except Exception as ex:
            print(f"Error during download: {ex}")
            header = "NOT FOUND\n"
            self.socket.send(header.encode('utf-8'))
    
    def handle_upload(self, file_name, parts):
        try:
            # Expecting header format: "upload filename filesize"
            if len(parts) < 3:
                header = "ERROR Invalid upload format\n"
                # I/O: socket.send(bytes)
                self.socket.send(header.encode('utf-8'))
                return
            
            file_size = int(parts[2])
            
            # Create ServerShare directory if it doesn't exist
            os.makedirs("ServerShare", exist_ok=True)
            
            file_path = os.path.join("ServerShare", file_name)
            
            # Read the file data
            bytes_received = 0
            file_data = bytearray()
            
            while bytes_received < file_size:
                chunk_size = min(4096, file_size - bytes_received)
                # I/O: bytes = socket.recv(n_bytes)
                chunk = self.socket.recv(chunk_size)
                if not chunk:
                    break
                file_data.extend(chunk)
                bytes_received += len(chunk)
            
            # Save the file
            with open(file_path, 'wb') as file_out:
                file_out.write(file_data)
            
            # Send success response
            header = "OK\n"
            # I/O: socket.send(bytes)
            self.socket.send(header.encode('utf-8'))
            
            print(f"File uploaded successfully: {file_name} ({file_size} bytes)")
            
        except Exception as ex:
            print(f"Error during upload: {ex}")
            header = "ERROR\n"
            self.socket.send(header.encode('utf-8'))


if __name__ == "__main__":
    # Note: Running on port 80 requires root/admin privileges
    # Using port 8080 for easier testing
    server = FxServer(port=8080)
    server.start()