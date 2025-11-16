import socket
# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
server_address = ('127.0.0.1', 65432)
client_socket.connect(server_address)

# Input from user
num1 = input("Enter first integer: ")
num2 = input("Enter second integer: ")
op = input("Enter operation (+, -, *, /, %): ")

# Send data to server
message = f"{num1} {num2} {op}"
client_socket.send(message.encode())

# Receive result from server
result = client_socket.recv(1024).decode()
print("Result from server:", result)

client_socket.close()
