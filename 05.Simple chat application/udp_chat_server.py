import socket

HOST = '127.0.0.1'
PORT = 7000
BUFFER_SIZE = 1000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"UDP Server listening on {HOST}:{PORT}")

try:
    # Receive initial message to know client address
    data, client_addr = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Client ({client_addr}): {data.decode()}")

    while True:
        # Send reply
        reply = input("Server: ")
        server_socket.sendto(reply.encode(), client_addr)

        # Receive next message
        data, client_addr = server_socket.recvfrom(BUFFER_SIZE)
        print(f"Client ({client_addr}): {data.decode()}")

except KeyboardInterrupt:
    print("\nChat stopped.")

finally:
    server_socket.close()
