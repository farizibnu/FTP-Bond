import socket
import os

def upload_file(client_socket, filename):
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        client_socket.send(f"UPLOAD {filename} {filesize}".encode())
        with open(filename, 'rb') as f:
            data = f.read(filesize)
            client_socket.sendall(data)
        response = client_socket.recv(1024).decode()
        print(response)
    else:
        print(f"File {filename} not found.")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    
    while True:
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filename = input("Enter the filename to upload: ")
            upload_file(client_socket, filename)
        elif choice == '2':
            client_socket.send("EXIT".encode())
            break
        else:
            print("Invalid choice. Please try again.")
    
    client_socket.close()

if __name__ == "__main__":
    main()
