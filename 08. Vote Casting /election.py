import socket
import struct

# --- Configuration ---
MCAST_GROUP = '224.1.1.2'
MCAST_PORT = 10001
NUM_ELECTORATES = 5
# ---------------------

# 1. Get user's name (must be unique)
my_name = input("Enter your unique name: ")

# 2. Create the multicast (UDP) socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. Bind to the port
sock.bind(('', MCAST_PORT))

# 4. Tell the OS to join the multicast group
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"--- Joined election. {NUM_ELECTORATES} voters required. ---")

# 5. Get this user's vote
while True:
    vote = input("Cast your vote (A/B): ").strip().upper()
    if vote == 'A' or vote == 'B':
        break
    print("Invalid. Must be 'A' or 'B'.")

# 6. Send the vote to the group (format: "Name:Vote")
message = f"{my_name}:{vote}"
sock.sendto(message.encode(), (MCAST_GROUP, MCAST_PORT))
print(f"You voted '{vote}'. Waiting for other voters...")

# 7. Receive all votes (including your own)
votes_received = {} # Use a dictionary to store one vote per person

while len(votes_received) < NUM_ELECTORATES:
    data, addr = sock.recvfrom(1024)
    message = data.decode()
    
    try:
        # Parse "Name:Vote"
        voter_name, voter_vote = message.split(':')
        
        # Add their vote if we don't have it yet
        if voter_name not in votes_received:
            votes_received[voter_name] = voter_vote
            print(f"Got vote from {voter_name}. Total: {len(votes_received)}/{NUM_ELECTORATES}")
            
    except ValueError:
        print(f"Received invalid message: {message}")

# --- All votes are in! ---
print("\n--- ELECTION OVER: All votes received! ---")
print(f"Final Tally: {votes_received}")

# 8. Tally the results
votes_for_A = 0
votes_for_B = 0
for v in votes_received.values():
    if v == 'A':
        votes_for_A += 1
    elif v == 'B':
        votes_for_B += 1

# 9. Determine the winner
print(f"\nVotes for A: {votes_for_A}")
print(f"Votes for B: {votes_for_B}")

if votes_for_A > votes_for_B:
    print("WINNER: Candidate A")
elif votes_for_B > votes_for_A:
    print("WINNER: Candidate B")
else:
    print("RESULT: A Tie!")

# 10. Clean up
sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
sock.close()