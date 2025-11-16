import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

f = open("test.txt", "r")

for line in f:
    s.sendto(line.encode(), ("127.0.0.1", 6000))

s.sendto(b"END", ("127.0.0.1", 6000))

f.close()
s.close()
print("File sent (UDP).")