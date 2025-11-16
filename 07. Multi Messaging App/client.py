# Save this file as: client.py
# this version is only for terminal base multi message application
import socket
import threading
import sys

# --- Configuration ---
# You must change this to the IP address of the computer
# running the server.
# If testing on your own machine, use '127.0.0.1' (localhost)
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50000

# --- Functions ---

def receive_messages(sock):
    """
    This function runs in a separate thread
    Its only job is to listen for messages from the server.
    """
    while True:
        try:
            # Wait to receive data from the server
            message = sock.recv(1024).decode('utf-8')

            if not message:
                # Server disconnected
                print("\n[Disconnected from server. Press ENTER to exit.]")
                break

            # Print the message and re-draw the "You: " prompt
            print(f"\n{message}")
            print("You: ", end="", flush=True)

        except Exception as e:
            print(f"\n[Error receiving message: {e}]")
            break

def start_client(username):
    """
    The main function to start the client.
    """
    # 1. Create the client socket (TCP)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Try to connect to the server
    try:
        client.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"[Error: Could not connect to {SERVER_IP}:{SERVER_PORT} - {e}]")
        print("[Is the server running? Is the IP correct?]")
        return

    print(f"[Connected to server as '{username}']")

    # 3. Start the receiver thread
    # This thread will just listen for incoming messages
    receiver_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    receiver_thread.start()

    # 4. Start the sender loop (in the main thread)
    # This loop waits for user input and sends it
    print("Type 'exit' to quit.")

    try:
        while True:
            # Wait for the user to type
            print("You: ", end="", flush=True)
            message = input()

            if message.lower() == 'exit':
                break

            # Format the message and send it to the server
            formatted_message = f"[{username}]: {message}"
            client.send(formatted_message.encode('utf-8'))

    except (EOFError, KeyboardInterrupt):
        print("\n[Disconnecting...]")
    finally:
        # 5. Clean up
        client.close()
        print("[Disconnected from server]")

if __name__ == "__main__":
    try:
        username = input("Enter your name: ")
        if not username:
            username = "Anonymous"
    except (EOFError, KeyboardInterrupt):
        sys.exit()
    start_client(username)