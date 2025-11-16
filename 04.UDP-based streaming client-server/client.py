import socket
import time

# Client configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
BUFFER_SIZE = 2048
OUTPUT_FILE = "received_media"

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request file from server
filename = input("Enter the multimedia filename to request: ")
client_socket.sendto(filename.encode(), (SERVER_IP, SERVER_PORT))

# Receive file chunks
with open(OUTPUT_FILE, "wb") as f:
    while True:
        data, _ = client_socket.recvfrom(BUFFER_SIZE)
        if not data:
            break  # End of file
        f.write(data)
        f.flush()  # Make bytes available for immediate access
        print(f"Received {len(data)} bytes")

print("File received. You can start playback now.")
client_socket.close()
