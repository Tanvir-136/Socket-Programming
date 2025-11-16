import socket

# --- Configuration ---
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 9000       # Port to listen on
# ---------------------

def perform_calculation(num1, op, num2):
    """Performs the calculation and returns the result as a string."""
    try:
        # Convert numbers from string to float for calculations
        n1 = float(num1)
        n2 = float(num2)
        
        if op == '+':
            result = n1 + n2
        elif op == '-':
            result = n1 - n2
        elif op == '*':
            result = n1 * n2
        elif op == '/':
            if n2 == 0:
                return "Error: Cannot divide by zero"
            result = n1 / n2
        elif op == '%':
            if n2 == 0:
                return "Error: Cannot modulo by zero"
            result = n1 % n2
        else:
            return "Error: Invalid operator"
            
        return str(result)
        
    except ValueError:
        return "Error: Invalid numbers"
    except Exception as e:
        return f"Error: {e}"

# 1. Create the main server TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    # 2. Bind and listen
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server listening on {HOST}:{PORT}")
    
    # 3. Main loop to accept new clients
    while True:
        # Wait for a client to connect
        conn, addr = server_socket.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        
        try:
            # 4. Loop to handle requests from this client
            while True:
                # 5. Receive the expression (e.g., "10 + 20")
                data = conn.recv(1024)
                if not data:
                    break # Client disconnected
                
                expression = data.decode().strip()
                print(f"[{addr}] Received: {expression}")
                
                # 6. Parse the expression
                try:
                    num1_str, op, num2_str = expression.split()
                    
                    # 7. Calculate the result
                    result_str = perform_calculation(num1_str, op, num2_str)
                    
                except ValueError:
                    result_str = "Error: Invalid format. Use 'num1 op num2'"
                
                # 8. Send the result back to the client
                conn.sendall(result_str.encode())
        
        except socket.error as e:
            print(f"[{addr}] Socket error: {e}")
        finally:
            # 9. Close connection when client disconnects
            conn.close()
            print(f"[{addr}] Connection closed.")

except KeyboardInterrupt:
    print("\n[STOPPING] Server is shutting down.")
finally:
    # 10. Close the main server socket
    server_socket.close()