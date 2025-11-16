# (Sends First)

import socket

# --- Configuration ---
MY_HOST = "0.0.0.0"
MY_PORT = 9002
PEER_IP = "127.0.0.1"
PEER_PORT = 9003
BUFFER_SIZE = 1024 # Max buffer size (for 1000 char limit)
# ---------------------

# 1. Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 2. Bind the socket
    sock.bind((MY_HOST, MY_PORT))
    print(f"UDP Peer 1 listening on {MY_HOST}:{MY_PORT}")
    print(f"Will send to {PEER_IP}:{PEER_PORT}")
    print("--- You (Peer 1) send the first message ---")
    
    # 3. Main chat loop
    while True:
        # --- Peer 1's Turn (Send) ---
        # Get input, limit to 1000 chars
        msg_send = input("You (Peer 1): ")[:1000]
        sock.sendto(msg_send.encode(), (PEER_IP, PEER_PORT))
        
        # --- Peer 1's Turn (Receive) ---
        # Wait for a reply
        msg_recv, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"Peer 2: {msg_recv.decode()}")

except KeyboardInterrupt:
    print("\n[EXITING] Chat stopped.")
finally:
    # 4. Close the socket
    sock.close()