import socket
import threading
import time

# --- Configuration ---
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8000
CHUNK_SIZE = 1000
SLEEP_TIME = 0.2  # 200ms
# ---------------------

def handle_client(conn, addr):
    """This function runs in its own thread for each client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # 1. Receive the filename
        filename_bytes = conn.recv(1024)
        filename = filename_bytes.decode().strip()
        print(f"[{addr}] Requested: {filename}")

        # 2. Try to open and send the file
        try:
            with open(filename, "rb") as f:
                # 3. Read and send in chunks
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break  # End of file
                    
                    conn.sendall(chunk)
                    time.sleep(SLEEP_TIME)
            
            print(f"[{addr}] Finished sending {filename}")
            
        except FileNotFoundError:
            # 4. Handle file not found
            print(f"[{addr}] File not found: {filename}")
            conn.sendall(b"ERROR: File not found")

    except socket.error as e:
        print(f"[{addr}] Socket error: {e}")
    finally:
        # 5. Close this client's connection
        conn.close()
        print(f"[{addr}] Connection closed.")

# --- Main Server Logic ---
if __name__ == "__main__":
    # 1. Create the main server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 2. Bind and listen
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[LISTENING] Server listening on {HOST}:{PORT}")
        
        # 3. Main loop to accept new clients
        while True:
            # Wait for a client
            conn, addr = server_socket.accept()
            
            # 4. Create and start a new thread for this client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt:
        print("\n[STOPPING] Server is shutting down.")
    finally:
        server_socket.close()