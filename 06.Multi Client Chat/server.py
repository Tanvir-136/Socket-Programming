import socket
import threading

# --- Configuration ---
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 9001       # Port to listen on
BUFFER_SIZE = 1024
# ---------------------

def handle_client(conn, addr):
    """
    This function is run by each thread.
    It handles one client's chat session.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # 4. Main chat loop for this client
        while True:
            # --- Server's Turn (Receive from this client) ---
            client_msg = conn.recv(BUFFER_SIZE).decode()
            if not client_msg:
                print(f"[{addr}] Client disconnected.")
                break
            
            # Identify which client sent the message
            print(f"Client {addr}: {client_msg}")
            
            # --- Server's Turn (Send to this client) ---
            # Get input from server admin.
            # Note: This input will be jumbled with other threads,
            # but it demonstrates the core concept for an exam.
            server_msg = input(f"Reply to {addr}: ")
            conn.sendall(server_msg.encode())

    except socket.error as e:
        print(f"[{addr}] Socket error: {e}")
    finally:
        # 5. Close the connection
        conn.close()
        print(f"[{addr}] Connection closed.")

# --- Main Server Logic ---
if __name__ == "__main__":
    # 1. Create the main server TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 2. Bind and listen
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[LISTENING] Server listening on {HOST}:{PORT}")
        
        # 3. Main loop to accept new clients
        while True:
            # Wait for a new client to connect
            conn, addr = server_socket.accept()
            
            # Create a new thread for this client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True # Allows server to exit (Ctrl+C)
            thread.start()

    except KeyboardInterrupt:
        print("\n[STOPPING] Server is shutting down.")
    finally:
        server_socket.close()