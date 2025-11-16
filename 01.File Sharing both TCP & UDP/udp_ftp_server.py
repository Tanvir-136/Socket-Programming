import socket

# --- Configuration ---
LISTEN_IP = "0.0.0.0"      # Listen on all available network interfaces
LISTEN_PORT = 6000       # Port to listen on (must match sender)
OUTPUT_FILENAME = "received_file.txt" # File to save received data
BUFFER_SIZE = 65535      # Max size of a UDP packet
# ---------------------

# 1. Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. "Bind" the socket to the IP and Port
# This tells the OS to send all incoming UDP data for this port to our script.
server_socket.bind((LISTEN_IP, LISTEN_PORT))

print(f"UDP server listening on {LISTEN_IP}:{LISTEN_PORT}...")

try:
    # 3. Open the output file in "write binary" (wb) mode
    with open(OUTPUT_FILENAME, "wb") as f:
        
        # 4. Loop forever, waiting for data
        while True:
            # Wait and "receive" a packet (up to BUFFER_SIZE bytes)
            # 'data' is the raw bytes received
            # 'addr' is the (IP, port) of the sender
            data, addr = server_socket.recvfrom(BUFFER_SIZE)

            # 5. Check if we received the "END" signal
            if data == b"END":
                print(f"Received END signal from {addr}. File transfer complete.")
                break  # Exit the loop
            
            # 6. If it's not "END", it's file data. Write it to the file.
            f.write(data)

    print(f"File saved as {OUTPUT_FILENAME}.")

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 7. Close the socket
    server_socket.close()
    print("Server shut down.")