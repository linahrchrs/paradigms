import socket
import sys
import os


SERVER_HOST = "localhost"
SERVER_PORT = 80
CLIENT_SHARE = "ClientShare"


def download_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        header = f"download {file_name}\n"
        sock.sendall(header.encode())

        # Read server response header
        response = sock.recv(1024).decode().strip()
        if response == "NOT FOUND":
            print("We're extremely sorry, the file you specified is not available!")
            return

        parts = response.split(" ")
        if parts[0] == "OK" and len(parts) >= 2:
            file_size = int(parts[1])
            received = b""

            while len(received) < file_size:
                chunk = sock.recv(min(4096, file_size - len(received)))
                if not chunk:
                    break
                received += chunk

            os.makedirs(CLIENT_SHARE, exist_ok=True)
            file_path = os.path.join(CLIENT_SHARE, file_name)
            with open(file_path, "wb") as f:
                f.write(received)

            print(f"File '{file_name}' downloaded successfully to {file_path}")
        else:
            print("You're not connected to the right Server!")


def upload_file(file_name):
    file_path = os.path.join(CLIENT_SHARE, file_name)
    if not os.path.exists(file_path):
        print(f"File '{file_name}' not found in {CLIENT_SHARE}")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        header = f"upload {file_name} {len(data)}\n"
        sock.sendall(header.encode())
        sock.sendall(data)

        response = sock.recv(1024).decode().strip()
        print(response)


def main():
    if len(sys.argv) < 3:
        print("Usage: python FxClient.py <command> <filename>")
        print("Commands: d = download, u = upload")
        return

    command = sys.argv[1]
    file_name = sys.argv[2]

    if command == "d":
        download_file(file_name)
    elif command == "u":
        upload_file(file_name)
    else:
        print("Unknown command. Use 'd' for download or 'u' for upload.")


if __name__ == "__main__":
    main()
