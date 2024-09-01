import hashlib
import base64

with open('htmx.min.js', 'rb') as f:
    file_hash = hashlib.sha256(f.read()).digest()
    base64_hash = base64.b64encode(file_hash).decode('utf-8')
    print(base64_hash)
