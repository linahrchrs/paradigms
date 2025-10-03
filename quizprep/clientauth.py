import argparse
from socket import create_connection

SERVER_ENDPOINT = ('localhost', 8080)
BUFFER = 4096

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str)
parser.add_argument("username", type=str)
parser.add_argument("password", type=str)
parser.add_argument("passwordconf", type=str)
args = parser.parse_args()

with create_connection(SERVER_ENDPOINT) as socket:
    user = args.username
    pwd = args.password

    if args.command == "LOGIN":
        header = f"LOGIN {user} {pwd}\n"
        socket.sendall(header.encode())
        response = socket.recv(1024).decode().strip()
        token, *rest = response.split(" ")
        if token != "ERROR":
            print ("SUCCESS\n")
        else:
            print("User not found\n")
    
    elif args.command == "LOGOUT":
        header = f"LOGOUT {user}\n"
        socket.sendall(header.encode())
        response = socket.recv(1024).decode().strip()
        token, *rest = response.split(" ")
        if token != "ERROR":
            print("Successfully logged out\n")
        else:
            print("User not logged in\n")
    
    elif args.command == "REGISTER":
        conf = args.passwordconf
        header = f"REGISTER {user} {pwd} {conf}\n"
        socket.sendall(header.encode())
        response = socket.recv(1024).decode().strip()
        token, *rest = response.split(" ")
        if token != "ERROR":
            print("REGISTERED\n")
        else:
            msg = rest[0]
            if msg == "UserAlreadyRegistered":
                print("User already exists in database\n")
            elif msg == "PwdConfNotMatch":
                print("Password confirmation doesn't match the password\n")
            else:
                print("Failed to register\n")
    
    else: 
        print("Wrong command!\n")
        