import socket

HOST = '127.0.0.1'
PORT = 6000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"TCP Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Receive message from client
        msg = conn.recv(1024).decode()
        if not msg:
            break
        print(f"Client: {msg}")

        # Send reply
        reply = input("Server: ")
        conn.send(reply.encode())

except KeyboardInterrupt:
    print("\nChat stopped.")

finally:
    conn.close()
    server_socket.close()
