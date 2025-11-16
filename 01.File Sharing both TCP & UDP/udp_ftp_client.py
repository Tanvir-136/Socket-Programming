import socket

# --- Configuration ---
TARGET_IP = "127.0.0.1"  # IP of the server (localhost)
TARGET_PORT = 6000       # Port the server is listening on
FILENAME = "test.txt"      # The file you want to send
# ---------------------

# 1. Create a UDP socket
#    AF_INET = IPv4
#    SOCK_DGRAM = UDP (Datagram)
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Sending {FILENAME} to {TARGET_IP}:{TARGET_PORT}...")

    # 2. Open the file in "read binary" (rb) mode.
    #    "rb" mode reads the file as raw bytes, which is what sockets send.
    with open(FILENAME, "rb") as f:
        # 3. Read the file line by line
        for line in f:
            # 'line' is already bytes (because we used "rb")
            # We send each line as one UDP packet
            client_socket.sendto(line, (TARGET_IP, TARGET_PORT))
    
    # 4. Send a special "END" message
    # This tells the server that we are finished.
    client_socket.sendto(b"END", (TARGET_IP, TARGET_PORT))

    print("File sent successfully.")

except FileNotFoundError:
    print(f"Error: File '{FILENAME}' not found.")
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 5. Close the socket
    if 'client_socket' in locals():
        client_socket.close()