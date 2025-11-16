import socket
import threading
import time

def handle_client(conn, filename):
    try:
        f = open(filename, "rb")
    except:
        conn.send(b"ERROR: File not found")
        conn.close()
        return

    while True:
        data = f.read(1000)    # 1000 bytes per flush
        if not data:
            break
        conn.send(data)
        time.sleep(0.2)        # 200 ms sleep

    f.close()
    conn.close()
    print(f"Finished sending {filename}")

def client_thread(conn):
    filename = conn.recv(1024).decode().strip()
    print("Client requested:", filename)

    t = threading.Thread(target=handle_client, args=(conn, filename))
    t.start()

server = socket.socket()
server.bind(("0.0.0.0", 7000))
server.listen(5)

print("Concurrent File Server running...")

while True:
    conn, addr = server.accept()
    print("Client connected:", addr)
    threading.Thread(target=client_thread, args=(conn,)).start()
