import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 6000))

print("UDP Server ready...")
f = open("rec_udp.txt", "w")

while True:
    data, addr = s.recvfrom(1024)
    if data == b"END":
        break
    f.write(data.decode())
    f.flush()
f.close()
s.close()
print("File received.")
