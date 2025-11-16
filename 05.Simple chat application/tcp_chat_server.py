import socket

# --- Configuration ---
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 9001       # Port to listen on
BUFFER_SIZE = 1024
# ---------------------

# 1. Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    # 2. Bind and listen
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")
    
    # 3. Wait for a client to connect
    conn, addr = server_socket.accept()
    print(f"[CONNECTED] Client connected from {addr}")

    with conn:
        # 4. Main chat loop
        while True:
            # --- Server's Turn (Receive) ---
            # Wait for the client to send a message
            client_msg = conn.recv(BUFFER_SIZE).decode()
            if not client_msg:
                print("[CLIENT DISCONNECTED]")
                break
            print(f"Client: {client_msg}")
            
            # --- Server's Turn (Send) ---
            # Get input from server user and send it
            server_msg = input("Server: ")
            conn.sendall(server_msg.encode())

except KeyboardInterrupt:
    print("\n[STOPPING] Server is shutting down.")
finally:
    # 5. Close the socket
    server_socket.close()