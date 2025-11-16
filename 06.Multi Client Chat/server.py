import socket
import threading

HOST = '127.0.0.1'
PORT = 6000

# Function to handle each client
def handle_client(conn, addr):
    print(f"New connection from {addr}")
    try:
        while True:
            # Receive message from client
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"Client {addr}: {msg}")

            # Send reply to client
            reply = input(f"Reply to {addr}: ")
            conn.send(reply.encode())
    except KeyboardInterrupt:
        print(f"\nChat with {addr} stopped.")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
except KeyboardInterrupt:
    print("\nServer shutting down.")
finally:
    server_socket.close()