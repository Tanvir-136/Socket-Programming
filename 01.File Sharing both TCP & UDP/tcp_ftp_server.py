import socket

LISTEN_IP = "0.0.0.0"      
LISTEN_PORT = 7000      
OUTPUT_FILENAME = "received_file_tcp.txt"
BUFFER_SIZE = 1024       

ser_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    ser_soc.bind((LISTEN_IP, LISTEN_PORT))
    ser_soc.listen(1) 
    print(f"TCP server listening on {LISTEN_IP}:{LISTEN_PORT}...")

    conn, addr = ser_soc.accept()
    

    with conn:      # Use 'with' to auto-close the connection socket
        print(f"Connected by {addr}")
        with open(OUTPUT_FILENAME, "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    print("Client disconnected (no END signal).")
                    break
                
                if data == b"END":
                    print("Received END signal. Transfer complete.")
                    break
                
                # 9. If it's file data, write it
                f.write(data)
                
                # 10. Send the Acknowledgment (ACK)
                print(f"Received chunk ({len(data)} bytes). Sending ACK.")
                conn.sendall(b"ACK")
                
    print(f"File saved as {OUTPUT_FILENAME}.")

except socket.error as e:
    print(f"Socket error: {e}")
finally:
    # 11. Close the main server socket
    ser_soc.close()
    print("Server shut down.")