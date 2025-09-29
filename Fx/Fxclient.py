import socket
import sys
import os

class FxClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
    
    def download(self, file_name):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_to_server:
                connection_to_server.connect((self.host, self.port))
                
                in_stream = connection_to_server.makefile('rb')
                out_stream = connection_to_server.makefile('wb')
                
                # Send download request
                header = f"download {file_name}\n"
                out_stream.write(header.encode('utf-8'))
                out_stream.flush()
                
                # Read response header
                response = in_stream.readline().decode('utf-8').strip()
                
                if response == "NOT FOUND":
                    print("We're extremely sorry, the file you specified is not available!")
                else:
                    parts = response.split(' ')
                    status = parts[0]
                    
                    if status == "OK":
                        if len(parts) < 2:
                            print("Invalid server response!")
                            return
                        
                        size = int(parts[1])
                        
                        # Read file data
                        bytes_received = 0
                        space = bytearray()
                        
                        while bytes_received < size:
                            chunk_size = min(4096, size - bytes_received)
                            chunk = connection_to_server.recv(chunk_size)
                            if not chunk:
                                break
                            space.extend(chunk)
                            bytes_received += len(chunk)
                        
                        # Create ClientShare directory if it doesn't exist
                        os.makedirs("ClientShare", exist_ok=True)
                        
                        # Save file
                        file_path = os.path.join("ClientShare", file_name)
                        with open(file_path, 'wb') as file_out:
                            file_out.write(space)
                        
                        print(f"File downloaded successfully: {file_name} ({size} bytes)")
                    else:
                        print("You're not connected to the right Server!")
        
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure the server is running.")
        except Exception as e:
            print(f"Error during download: {e}")
    
    def upload(self, file_name):
        try:
            # Check if file exists
            if not os.path.exists(file_name):
                print(f"Error: File '{file_name}' not found!")
                return
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_to_server:
                connection_to_server.connect((self.host, self.port))
                
                in_stream = connection_to_server.makefile('rb')
                out_stream = connection_to_server.makefile('wb')
                
                # Read file data
                with open(file_name, 'rb') as file_in:
                    file_data = file_in.read()
                    file_size = len(file_data)
                
                # Extract just the filename (not the path)
                base_name = os.path.basename(file_name)
                
                # Send upload request with filename and size
                header = f"upload {base_name} {file_size}\n"
                out_stream.write(header.encode('utf-8'))
                out_stream.flush()
                
                # Send file data
                connection_to_server.sendall(file_data)
                
                # Read response
                response = in_stream.readline().decode('utf-8').strip()
                
                if response == "OK":
                    print(f"File uploaded successfully: {base_name} ({file_size} bytes)")
                elif response.startswith("ERROR"):
                    print(f"Upload failed: {response}")
                else:
                    print("You're not connected to the right Server!")
        
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure the server is running.")
        except Exception as e:
            print(f"Error during upload: {e}")
    
    def list_files(self):
        """Bonus feature: List files on the server"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_to_server:
                connection_to_server.connect((self.host, self.port))
                
                in_stream = connection_to_server.makefile('rb')
                out_stream = connection_to_server.makefile('wb')
                
                # Send list request
                header = "list\n"
                out_stream.write(header.encode('utf-8'))
                out_stream.flush()
                
                # Read response
                response = in_stream.readline().decode('utf-8').strip()
                print(f"Server response: {response}")
        
        except Exception as e:
            print(f"Error listing files: {e}")


def print_usage():
    print("Usage:")
    print("  Download: python fx_client.py d <filename>")
    print("  Upload:   python fx_client.py u <filename>")
    print("  List:     python fx_client.py l")
    print("\nExamples:")
    print("  python fx_client.py d document.txt")
    print("  python fx_client.py u myfile.pdf")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    client = FxClient(host='localhost', port=8080)
    
    if command == "d":
        if len(sys.argv) < 3:
            print("Error: Please specify a filename to download")
            print_usage()
            sys.exit(1)
        file_name = sys.argv[2]
        client.download(file_name)
    
    elif command == "u":
        if len(sys.argv) < 3:
            print("Error: Please specify a filename to upload")
            print_usage()
            sys.exit(1)
        file_name = sys.argv[2]
        client.upload(file_name)
    
    elif command == "l":
        client.list_files()
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)