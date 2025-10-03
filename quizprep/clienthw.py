from socket import create_connection
import argparse
import sys

SERVER_ENDPOINT = ("localhost", 7500)
BUFFER = 4096

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str)
parser.add_argument("filename", type=str)
parser.add_argument("type", type=str)
args = parser.parse_args()

try:
    with create_connection(SERVER_ENDPOINT) as socket:
        
        if args.command == "list":
            # Request list of available log files
            header = "LIST\n"
            socket.sendall(header.encode())
            
            response = socket.recv(BUFFER).decode().strip()
            lines = response.split("\n")
            token = lines[0].split()[0]
            
            if token == "OK":
                num_files = int(lines[0].split()[1])
                print(f"Available log files ({num_files}):")
                for i in range(1, num_files + 1):
                    print(f" {lines[i]}")
            else:
                print(response)
        
        elif args.command == "analyze":
            if not args.filename or not args.type:
                print("Error: filename and type required for analyze command")
                sys.exit(1)
            
            # Request log analysis
            header = f"ANALYZE {args.filename} {args.type}\n"
            socket.sendall(header.encode())
            
            response = socket.recv(BUFFER).decode().strip()
            lines = response.split("\n")
            token = lines[0].split()[0]
            
            if token == "OK":
                if args.type == "COUNT":
                    count = lines[0].split()[1]
                    print(f"Total requests in {args.filename}: {count}")
                elif args.type == "STATUS":
                    num_codes = int(lines[0].split()[1])
                    print(f"Status code distribution for {args.filename}:")
                    for i in range(1, num_codes + 1):
                        parts = lines[i].split()
                        print(f"  {parts[0]}: {parts[1]} requests")
            else:
                print(response)
        
        elif args.command == "download":
            if not args.filename:
                print("Error: filename required for download command")
                sys.exit(1)
            
            # Request log file download
            header = f"DOWNLOAD {args.filename}\n"
            socket.sendall(header.encode())
            
            msg = socket.recv(1024).decode().strip()
            token, *rest = msg.split(" ")
            
            if token == "OK":
                file_size = int(rest[0])
                file_content = b""
                
                while len(file_content) < file_size:
                    chunk = socket.recv(BUFFER)
                    if not chunk:
                        break
                    file_content += chunk
                
                output_filename = f"downloaded {args.filename}"
                with open(output_filename, "wb") as file:
                    file.write(file_content)
                
                print(f"File downloaded successfully: {output_filename}")
            else:
                print(msg)

except ConnectionRefusedError:
    print("Error: Cannot connect to server. Make sure the server is running.")
except Exception as e:
    print(f"Error: {e}")