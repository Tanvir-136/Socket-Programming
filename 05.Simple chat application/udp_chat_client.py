import socket

HOST = '127.0.0.1'
PORT = 7000
BUFFER_SIZE = 1000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send initial message to server
    msg = input("Client: ")
    client_socket.sendto(msg.encode(), (HOST, PORT))

    while True:
        # Receive reply
        data, server_addr = client_socket.recvfrom(BUFFER_SIZE)
        print(f"Server ({server_addr}): {data.decode()}")

        # Send next message
        msg = input("Client: ")
        client_socket.sendto(msg.encode(), (HOST, PORT))

except KeyboardInterrupt:
    print("\nChat stopped.")

finally:
    client_socket.close()
