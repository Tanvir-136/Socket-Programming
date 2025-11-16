import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000
# ---------------------

# 1. Create a client TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2. Connect to the server
    print(f"Connecting to server at {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected. (Type 'exit' as first number to quit)")

    # 3. Main loop to send expressions
    while True:
        # 4. Get input from the user
        num1 = input("Enter first number: ")
        if num1.lower() == 'exit':
            break
        
        op = input("Enter operator (+, -, *, /, %): ")
        num2 = input("Enter second number: ")

        # 5. Format the expression as a string
        expression = f"{num1} {op} {num2}"
        
        # 6. Send the expression to the server
        client_socket.sendall(expression.encode())
        
        # 7. Wait for and receive the result
        result = client_socket.recv(1024).decode()
        
        # 8. Display the result
        print(f"Server result: {result}\n")

except socket.error as e:
    print(f"Socket error: {e}")
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # 9. Close the socket
    client_socket.close()
    print("Connection closed.")