# Socket

Minimal, focused TCP client/server example.

## Quick start
Requirements: Python 3.7+

Install:
```bash
git clone https://github.com/Tanvir-136/Socket-Programming.git
```bash
# optional: create and activate a virtualenv, then install deps if requirements.txt exists
python -m venv .venv
source .venv/bin/activate
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi
```
```

Run:
```bash
# start server
python server.py

# start client (in another terminal)
python client.py
```

## Features
- Lightweight TCP client & server examples
- Small utilities for testing and learning