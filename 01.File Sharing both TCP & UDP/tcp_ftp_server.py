import socket

s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen(1)

print("Server ready...")
conn, addr = s.accept()
print("Connected:", addr)

f = open("test.txt", "wb")

while True:
    data = conn.recv(1024)
    if not data:
        break
    
    f.write(data)
    conn.send(b"ACK")  # acknowledgment

f.close()
conn.close()
s.close()
print("File received.")
