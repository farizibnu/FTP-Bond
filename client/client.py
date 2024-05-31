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

def download_file(client_socket, filename):
    client_socket.send(f"DOWNLOAD {filename}".encode())
    response = client_socket.recv(1024).decode()
    if response.startswith("READY"):
        filesize = int(response.split()[1])
        with open(f"downloaded_{filename}", 'wb') as f:
            data = client_socket.recv(filesize)
            f.write(data)
        print(f"File {filename} downloaded successfully.")
    else:
        print(response)

def print_menu():
    print("1. Upload file")
    print("2. Download file")
    print("3. Exit")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            filename = input("Enter the filename to upload: ")
            upload_file(client_socket, filename)
        elif choice == '2':
            filename = input("Enter the filename to download: ")
            download_file(client_socket, filename)
        elif choice == '3':
            client_socket.send("EXIT".encode())
            break
        else:
            print("Invalid choice. Please try again.")
    
    client_socket.close()

if __name__ == "__main__":
    main()
