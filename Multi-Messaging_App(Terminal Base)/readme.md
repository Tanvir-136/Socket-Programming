# Multi-Messaging App (Terminal)

## Quick start
1. Open one terminal and start the server:
```bash
python3 server.py [--group 224.0.0.1] [--port 5007]
```
2. Open one terminal per user and start the client:
```bash
python3 client.py --name <nickname> [--group 224.0.0.1] [--port 5007] [--iface <interface>]
```

## Requirements
- Python 3.7+
- Network with UDP multicast support (localhost works for single-machine tests)

## Usage
### Server:
```bash
python3 server.py [--group <multicast_ip>] [--port <port>]
```

### Client:
```bash
python3 client.py --name <nickname> [--group <multicast_ip>] [--port <port>] [--iface <interface>]
```

## Defaults (good for beginners)
- group: 224.0.0.1
- port: 5007

## Examples
- Start server:
```bash
python3 server.py
```
- Start Alice:
```bash
python3 client.py --name alice
```
- Start Bob (another terminal):
```bash
python3 client.py --name bob
```

## How it works (short)
- Run the server once to host the multicast/relay.
- Run one client per participant; clients send messages to the server/group and receive messages from others.
- Each client shows the sender nickname so conversations are clear.

## Tips & troubleshooting
- Use multicast addresses in 224.0.0.0–239.255.255.255.
- If messages don’t appear across machines: check firewall, multicast routing, and interface binding.
- For local testing, bind to loopback or omit --iface.

## Security & limits
- No encryption or authentication; avoid untrusted networks.

## License
This project is licensed under the MIT License. See the LICENSE file at the repository root for the full text.
