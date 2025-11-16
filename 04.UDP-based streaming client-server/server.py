import socket
import random
import os

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 9000
BUFFER_SIZE = 65535 # Max UDP packet size
# ---------------------

# 1. Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 2. Bind the socket
    server_socket.bind((HOST, PORT))
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")

    # 3. Wait for a client to request a file
    # This first packet will be the filename
    try:
        data, client_addr = server_socket.recvfrom(BUFFER_SIZE)
        filename = data.decode().strip()
        print(f"[{client_addr}] Requested file: {filename}")

        # --- Security Check ---
        if ".." in filename or "/" in filename or "\\" in filename:
            print(f"[{client_addr}] Invalid filename request.")
            server_socket.sendto(b"ERROR: Invalid filename", client_addr)
            raise Exception("Invalid filename") # Go to finally, don't crash

        # 4. Try to open the file and stream it
        try:
            with open(filename, "rb") as f:
                # 5. Loop to read and send the file
                while True:
                    # 6. Read a chunk of a random size (1000-2000 bytes)
                    chunk_size = random.randint(1000, 2000)
                    chunk = f.read(chunk_size)
                    
                    if not chunk:
                        # End of file
                        break
                    
                    # 7. Send the chunk to the client
                    server_socket.sendto(chunk, client_addr)
            
            # 8. Send a special "END" message
            server_socket.sendto(b"END_OF_STREAM", client_addr)
            print(f"[{client_addr}] Finished streaming {filename}.")
        
        except FileNotFoundError:
            print(f"[{client_addr}] File not found: {filename}")
            server_socket.sendto(b"ERROR: File not found", client_addr)
            
    except Exception as e:
        print(f"An error occurred: {e}")

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 9. Close the socket
    server_socket.close()
    print("[STOPPING] Server shut down.")