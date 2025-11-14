# Save this file as: server.py
# this version is only for terminal base multi message application

import socket
import threading

# --- Configuration ---
HOST = '0.0.0.0' # Listen on all available network interfaces
PORT = 50000     # The same port as our multicast chat

# --- State ---
# We need to keep track of all connected clients
# We also need a "lock" to safely add/remove clients
# from the list, since threads will be doing this.
clients = []
clients_lock = threading.Lock()

# --- Functions ---
def broadcast(message, sender_socket):
    """
    Sends a message to all clients *except* the one who sent it.
    """
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # If sending fails, the client is likely disconnected
                    # We'll remove them in the handle_client loop
                    pass

def handle_client(client_socket):
    """
    This function runs in a new thread for each client.
    It listens for messages from its client and broadcasts them.
    """
    print(f"[New connection from {client_socket.getpeername()}]")

    # Add the new client to our list
    with clients_lock:
        clients.append(client_socket)

    try:
        while True:
            # Wait to receive a message from this client
            # 1024 bytes buffer
            message = client_socket.recv(1024)

            if not message:
                # If we receive empty data, the client has disconnected
                break

            print(f"[Message received from {client_socket.getpeername()}]")
            # Send the received message to all *other* clients
            broadcast(message, client_socket)

    except Exception as e:
        print(f"[Error with {client_socket.getpeername()}: {e}]")

    finally:
        # When the loop breaks (client disconnected), remove them
        with clients_lock:
            clients.remove(client_socket)

        print(f"[Connection from {client_socket.getpeername()} closed]")
        client_socket.close()

def main():
    """
    The main function to start the server.
    """
    # Create the server socket
    # AF_INET = use IPv4
    # SOCK_STREAM = use TCP (a reliable "stream" connection)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # This allows us to re-run the server quickly after closing it
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the server to our host and port
    try:
        server.bind((HOST, PORT))
    except Exception as e:
        print(f"[Error: Could not bind to {HOST}:{PORT} - {e}]")
        return

    # Start listening for incoming connections
    server.listen(5) # Allow up to 5 queued connections
    print(f"[*] Chat server started on {HOST}:{PORT}")

    # Main loop to accept new clients
    while True:
        try:
            # Wait for a new client to connect
            # This is a "blocking" call
            client_socket, addr = server.accept()

            # When a client connects, start a new thread to handle them
            # This way, we can handle multiple clients at once
            # The 'main' thread just goes back to waiting for connections
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True # Allows the program to exit
            thread.start()

        except KeyboardInterrupt:
            print("\n[Server shutting down...]")
            break

    # Clean up
    server.close()
    with clients_lock:
        for client in clients:
            client.close()

if __name__ == "__main__":
    main()
