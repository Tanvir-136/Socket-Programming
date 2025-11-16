import socket

HOST = '127.0.0.1'
PORT = 6000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to TCP Server at {HOST}:{PORT}")

try:
    while True:
        # Send message
        msg = input("Client: ")
        client_socket.send(msg.encode())

        # Receive reply
        reply = client_socket.recv(1024).decode()
        print(f"Server: {reply}")

except KeyboardInterrupt:
    print("\nChat stopped.")

finally:
    client_socket.close()
