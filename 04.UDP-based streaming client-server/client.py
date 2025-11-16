import socket

# --- Configuration ---
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000
FILE_TO_REQUEST = "sample.mp4"  # IMPORTANT: Must match a file on the server
BUFFER_SIZE = 65535 # Max UDP packet size (must be larger than 2000)
# ---------------------

# 1. Create a client UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout for receiving data (e.g., 5 seconds)
client_socket.settimeout(5.0)

# 2. Define the output filename
output_filename = "downloaded_" + FILE_TO_REQUEST

try:
    # 3. Send the filename request to the server
    print(f"Requesting '{FILE_TO_REQUEST}' from {SERVER_IP}:{SERVER_PORT}...")
    client_socket.sendto(FILE_TO_REQUEST.encode(), (SERVER_IP, SERVER_PORT))

    # 4. Open the output file in "write binary" mode
    with open(output_filename, "wb") as f:
        
        # 5. Loop to receive the file chunks
        while True:
            try:
                # 6. Wait for a packet
                data, server_addr = client_socket.recvfrom(BUFFER_SIZE)
                
                # 7. Check for the "END" signal
                if data == b"END_OF_STREAM":
                    print("\nStream complete.")
                    break
                
                # 8. Check for an error message
                if data.startswith(b"ERROR:"):
                    print(f"\nServer error: {data.decode()}")
                    break
                
                # 9. Write the received data chunk to the file
                f.write(data)
                
                # Simple progress indicator
                print(f"Received chunk ({len(data)} bytes)", end='\r')

            except socket.timeout:
                print("\nServer timeout. No data received.")
                break

    print(f"File saved as {output_filename}.")
    print("Tip: You can often open this file in a media player (like VLC) *while* it is downloading.")

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 10. Close the socket
    client_socket.close()