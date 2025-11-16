import socket
import time

# --- Configuration ---
SERVER_IP = "127.0.0.1"
SERVER_PORT = 7000
FILENAME = "test.txt"
CHUNK_SIZE = 100
TIMEOUT = 3  # Timeout in seconds
# ---------------------

# 1. Create a TCP/IP socket
#    AF_INET = IPv4
#    SOCK_STREAM = TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2. Connect to the server
    print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected.")

    # 3. Set a timeout for socket operations (like recv)
    client_socket.settimeout(TIMEOUT)

    # 4. Open the file in "read binary" (rb) mode
    with open(FILENAME, "rb") as f:
        
        # 5. Loop to read the file in chunks
        while True:
            # Read a chunk from the file
            chunk = f.read(CHUNK_SIZE)
            
            # If the chunk is empty, we've reached the end of the file
            if not chunk:
                break
            
            ack_received = False
            
            # 6. Loop for retransmission (in case of timeout)
            while not ack_received:
                try:
                    # 7. Send the chunk
                    print(f"Sending chunk ({len(chunk)} bytes)...")
                    client_socket.sendall(chunk)
                    
                    # 8. Wait for an Acknowledgment (ACK)
                    ack = client_socket.recv(1024) # Buffer size for ACK
                    
                    if ack == b"ACK":
                        print("ACK received.")
                        ack_received = True # Move to the next chunk
                    
                except socket.timeout:
                    print(f"TIMEOUT. No ACK received. Retransmitting chunk...")
                    # The loop will repeat, re-sending the same chunk
    
    # 9. Send a special "END" message when done
    print("File transfer complete. Sending END signal.")
    client_socket.sendall(b"END")

except FileNotFoundError:
    print(f"Error: File '{FILENAME}' not found.")
except socket.timeout:
    print("Connection timed out (initial connection).")
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 10. Close the socket
    client_socket.close()
    print("Connection closed.")