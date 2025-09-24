# main.py
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,  # points to this file
        host="0.0.0.0",
        port=3001,
    )