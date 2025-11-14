# Socket

Simple project demonstrating socket usage.

## Description
Minimal socket example and utilities.

## Features
- TCP client/server example
- Simple message exchange

## Requirements
- Python 3.7+
- (or specify your language/runtime)

## Installation
```bash
git clone <repo-url> socket
cd socket
# optionally create a virtual env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run the server and client (example):
```bash
python server.py
python client.py
```

## Screenshot (embedded)
This README can contain the screenshot image inline as a data URI so no external asset file is required.

Example using an embedded PNG (1×1 transparent placeholder shown here — replace <BASE64_DATA> with your image's base64):

![Socket example screenshot](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=)

To embed your own image:
1. Convert your image to base64:
    - Linux: `base64 -w 0 /path/to/image.png > encoded.txt`
    - macOS: `base64 -b 0 /path/to/image.png > encoded.txt` or `openssl base64 -A -in /path/to/image.png > encoded.txt`
2. Open `encoded.txt`, copy the single-line base64 string and replace the data after `data:image/png;base64,` in the image link above.

For SVG you can also inline a URL-encoded or base64-encoded SVG with `data:image/svg+xml;utf8,` or `data:image/svg+xml;base64,`.

## License
Specify your license (e.g., MIT).