import socket
import time

s = socket.socket()
s.settimeout(2)   # timeout 2 seconds
s.connect(("127.0.0.1", 5000))

f = open("test.txt", "rb")

while True:
    block = f.read(100)       # 100 bytes per block
    if not block:
        break
    
    while True:
        try:
            s.send(block)
            ack = s.recv(3)
            if ack == b"ACK":
                break
        except socket.timeout:
            print("Timeout! Resending block...")
            continue

f.close()
s.close()
print("File sent successfully.")
