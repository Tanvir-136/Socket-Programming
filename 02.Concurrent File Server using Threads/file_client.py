import socket

s = socket.socket()
s.connect(("127.0.0.1", 7000))

filename = input("Enter filename: ")
s.send(filename.encode())

while True:
    data = s.recv(1024)
    if not data:
        break
    print(data.decode("utf-8", errors="ignore"), end="")

s.close()
