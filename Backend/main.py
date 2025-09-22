# main.py
import uvicorn
from app.main import app
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FULLCHAIN_DIR = os.path.join(BASE_DIR, "certs", "fullchain.pem")
PRIVKEY_DIR = os.path.join(BASE_DIR, "certs", "privkey.pem")

if __name__ == "__main__":
    uvicorn.run(
        app,  # points to this file
        host="0.0.0.0",
        port=3001,
        ssl_certfile=FULLCHAIN_DIR,
        ssl_keyfile=PRIVKEY_DIR
    )