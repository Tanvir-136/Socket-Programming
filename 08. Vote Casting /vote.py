import socket
import struct
import threading
import random
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
NUM_ELECTORATES = 5

votes_received = []

# Function to receive votes
def receive_votes(sock):
    while len(votes_received) < NUM_ELECTORATES:
        data, addr = sock.recvfrom(1024)
        vote = data.decode()
        if vote not in votes_received:
            votes_received.append(vote)
            print(f"Received vote: {vote} from {addr}")

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the multicast port
sock.bind(('', MCAST_PORT))

# Join multicast group
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Randomly select vote for this electorate
my_vote = random.choice(['A', 'B'])
print(f"My vote: {my_vote}")

# Start thread to receive votes
recv_thread = threading.Thread(target=receive_votes, args=(sock,))
recv_thread.start()

# Wait a short time to allow other electorates to join
time.sleep(1)

# Send own vote as multicast
sock.sendto(my_vote.encode(), (MCAST_GRP, MCAST_PORT))

# Wait for all votes
recv_thread.join()

# Count votes
count_A = votes_received.count('A')
count_B = votes_received.count('B')

# Determine winner
if count_A > count_B:
    winner = 'A'
elif count_B > count_A:
    winner = 'B'
else:
    winner = 'Tie'

print(f"All votes: {votes_received}")
print(f"Winner: {winner}")