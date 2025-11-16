import socket

# --- Configuration ---
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9001
BUFFER_SIZE = 1024
# ---------------------

# 1. Create a client TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2. Connect to the server
    print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected.")
    
    # 3. Main chat loop
    while True:
        # --- Client's Turn (Send) ---
        # Get input from client user and send it
        client_msg = input("Client: ")
        if not client_msg:
            continue # Don't send empty messages
            
        client_socket.sendall(client_msg.encode())
        
        # --- Client's Turn (Receive) ---
        # Wait for the server's reply
        server_msg = client_socket.recv(BUFFER_SIZE).decode()
        if not server_msg:
            print("[SERVER DISCONNECTED]")
            break
        print(f"Server: {server_msg}")

except KeyboardInterrupt:
    print("\n[EXITING] Closing connection.")
except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 4. Close the socket
    client_socket.close()