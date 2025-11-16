import socket
import os

# --- Configuration ---
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8000
RECEIVE_BUFFER = 1024 # Buffer size for receiving
# ---------------------

def download_file(filename):
    """
    Connects to the server and downloads the requested file.
    """
    
    # 1. Create a client TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected.")
        
        # 3. Send the name of the file we want
        client_socket.sendall(filename.encode())
        
        # 4. Receive the first chunk of data
        first_chunk = client_socket.recv(RECEIVE_BUFFER)
        
        # 5. Check if the first chunk is an error message
        if not first_chunk:
            print("Server closed connection (file might be empty?).")
            return

        if first_chunk.startswith(b"ERROR:"):
            print(f"Server error: {first_chunk.decode()}")
            return
            
        # 6. If it's not an error, open the output file
        output_filename = "downloaded_" + filename
        
        # 'file_opened' flag to avoid creating empty files on error
        file_opened = False
        
        try:
            with open(output_filename, "wb") as f:
                file_opened = True
                
                # Write the first chunk we already received
                f.write(first_chunk)
                
                # 7. Loop to receive the rest of the file
                while True:
                    data = client_socket.recv(RECEIVE_BUFFER)
                    
                    # If recv returns empty bytes, the server closed the socket
                    if not data:
                        break
                        
                    f.write(data)
                    
            print(f"File download complete. Saved as {output_filename}")

        except Exception as e:
            print(f"Error writing to file: {e}")
            # If we had an error writing, delete the partial file
            if file_opened:
                os.remove(output_filename)

    except socket.timeout:
        print("Connection timed out.")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        # 8. Close the socket
        client_socket.close()
        print("Connection closed.")

# --- Start the client ---
if __name__ == "__main__":
    file_to_download = input("Enter the filename to download (e.g., file1.txt): ")
    if file_to_download:
        download_file(file_to_download)
    else:
        print("No filename entered.")