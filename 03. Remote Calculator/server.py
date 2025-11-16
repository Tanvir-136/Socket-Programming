import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost and a port
server_address = ('127.0.0.1', 65432)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print("Server is waiting for a connection...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    try:
        # Receive data from client
        data = conn.recv(1024).decode()
        if not data:
            break

        # Split received data into numbers and operator
        num1, num2, op = data.split()
        num1 = int(num1)
        num2 = int(num2)

        # Perform calculation
        result = None
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        elif op == '%':
            result = num1 % num2 if num2 != 0 else "Error: Division by zero"
        else:
            result = "Error: Invalid operation"

        # Send result back to client
        conn.send(str(result).encode())

    except Exception as e:
        conn.send(f"Error: {e}".encode())
    
    finally:
        conn.close()