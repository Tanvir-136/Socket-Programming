import socket
import threading
import struct

# --- Configuration ---
MCAST_GROUP = '224.1.1.1'  # A standard multicast "transient" address
MCAST_PORT = 10000         # The port all members will use
MESSAGE_BUFFER = 1024      # Buffer size for incoming messages
# ---------------------

def receiver(sock, username):
    """
    This function runs in a separate thread.
    It loops forever, listening for multicast messages.
    """
    while True:
        try:
            # Wait for a message
            data, addr = sock.recvfrom(MESSAGE_BUFFER)
            message = data.decode()

            
            # \r moves cursor to start of line
            # ' ' * 50 clears the line
            # \r moves cursor back to start
            print(f"\r{' ' * 50}\r", end="")
            
            # Print the received message
            print(message)

            print(f"{username}: ", end="", flush=True)
            
        except socket.error:
            # Socket was closed, thread can exit
            break
        except Exception as e:
            print(f"[RECEIVER ERROR] {e}")

# --- Main Program Logic ---
if __name__ == "__main__":
    
    # 1. Get a username
    username = input("Enter your name: ")
    
    # 2. Create the multicast (UDP) socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # 3. Allow multiple sockets to bind to the same port
    #    This is CRITICAL for multicast.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 4. Bind to the server port
    #    We bind to '' (all interfaces) and the multicast port
    sock.bind(('', MCAST_PORT))
    
    # 5. Tell the OS to join the multicast group
    #    We create a 'mreq' (multicast request) structure
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    # 6. Set the Time-to-Live (TTL) for outgoing packets
    #    1 = local network only
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    print(f"--- Joined multicast chat on {MCAST_GROUP}:{MCAST_PORT} ---")

    # 7. Start the receiver thread
    recv_thread = threading.Thread(target=receiver, args=(sock, username))
    recv_thread.daemon = True # Thread will exit when main program exits
    recv_thread.start()

    # 8. Start the sender loop (this runs in the main thread)
    try:
        while True:
            # Wait for user to type a message
            message = input(f"{username}: ")
            
            # Format the message with the username
            full_message = f"{username}: {message}"
            
            # Send the message to the *entire multicast group*
            sock.sendto(full_message.encode(), (MCAST_GROUP, MCAST_PORT))
            
    except KeyboardInterrupt:
        print("\nLeaving chat...")
    finally:
        # 9. Tell the OS to leave the multicast group
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        sock.close()