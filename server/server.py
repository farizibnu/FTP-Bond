import socket
import threading
import os
from queue import Queue

# Inisialisasi queue untuk IPC
upload_queue = Queue()
download_queue = Queue()
client_activity = {}

# Fungsi untuk menangani setiap client
# Parameter : 1.)Client socket 2.)Client Address
def handle_client(client_socket, client_address):
    global client_activity
    client_id = client_address[0] + ':' + str(client_address[1])
    thread_id = threading.get_ident() # get thread id
    print(f"Thread ID {thread_id} handling client {client_id}")
    client_activity[client_id] = {'thread_id': thread_id, 'upload': 0, 'download': 0}
    
    while True:
        # Terima perintah dari client
        command = client_socket.recv(1024).decode() # Get command from client
        if not command: # Handle error if command was null
            break
        
        if command.startswith('UPLOAD'): # Jika command yang dikirim client itu "UPLOAD" maka simpan file di server
            filename = command.split()[1]
            filesize = int(command.split()[2])
            with open(filename, 'wb') as f:
                data = client_socket.recv(filesize)
                f.write(data)
            upload_queue.put(client_id)
            client_socket.send(f"File {filename} uploaded successfully.".encode())
        
        elif command.startswith('DOWNLOAD'): # Jika command yang dikirim client itu "DOWNLOAD" maka kirim file ke client
            filename = command.split()[1]
            if os.path.exists(filename):
                filesize = os.path.getsize(filename)
                client_socket.send(f"READY {filesize}".encode())
                with open(filename, 'rb') as f:
                    data = f.read(filesize)
                    client_socket.sendall(data)
                download_queue.put(client_id)
            else:
                client_socket.send(f"File {filename} not found.".encode()) # Handle error jika file yang hendak di download tidak ada
        
        elif command == 'EXIT':
            break
    
    client_socket.close() # close socket

# Fungsi untuk mencatat aktivitas client
def track_activity():
    global client_activity
    while True:
        if not upload_queue.empty():
            client_id = upload_queue.get()
            if client_id in client_activity:
                client_activity[client_id]['upload'] += 1
        
        if not download_queue.empty():
            client_id = download_queue.get()
            if client_id in client_activity:
                client_activity[client_id]['download'] += 1

# Fungsi untuk menampilkan aktivitas client
def print_client_activity():
    global client_activity
    while True:
        command = input("Enter 'status' to see client activity: ")
        if command == 'status':
            print("Client Activity:")
            for client_id, activity in client_activity.items():
                print(f"Client {client_id} - Thread ID: {activity['thread_id']}, Uploads: {activity['upload']}, Downloads: {activity['download']}")

# Fungsi utama untuk menjalankan server
def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    
    # Thread untuk melacak aktivitas client
    tracking_thread = threading.Thread(target=track_activity)
    tracking_thread.daemon = True
    tracking_thread.start()

    # Thread untuk menampilkan aktivitas client
    activity_thread = threading.Thread(target=print_client_activity)
    activity_thread.daemon = True
    activity_thread.start()
    
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    server_main()
