import socket

# --- Configuration ---
MY_HOST = "0.0.0.0"
MY_PORT = 9003
PEER_IP = "127.0.0.1"
PEER_PORT = 9002
BUFFER_SIZE = 1024 # Max buffer size (for 1000 char limit)
# ---------------------

# 1. Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 2. Bind the socket
    sock.bind((MY_HOST, MY_PORT))
    print(f"UDP Peer 2 listening on {MY_HOST}:{MY_PORT}")
    print(f"Will send to {PEER_IP}:{PEER_PORT}")
    print("--- Waiting for Peer 1 to talk... ---")
    
    # 3. Main chat loop
    while True:
        # --- Peer 2's Turn (Receive) ---
        # Wait for a message
        msg_recv, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"Peer 1: {msg_recv.decode()}")
        
        # --- Peer 2's Turn (Send) ---
        # Get input, limit to 1000 chars
        msg_send = input("You (Peer 2): ")[:1000]
        sock.sendto(msg_send.encode(), (PEER_IP, PEER_PORT))

except KeyboardInterrupt:
    print("\n[EXITING] Chat stopped.")
finally:
    # 4. Close the socket
    sock.close()