from fastapi import HTTPException, Query, APIRouter, Security, status, Depends
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os
import logging
import uvicorn
from typing import Optional, List
import pandas as pd
import requests

# Load environment variables
load_dotenv()

# Define the name of the header where the API key will be sent
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("REST_API_KEY")
WEB_TOKEN = os.getenv("WEB_TOKEN")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

router = APIRouter(dependencies=[Depends(get_api_key)])


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "..", "Data", "loads.csv")

def search_loads(origin: Optional[str] = None):
    # Read CSV into a DataFrame
    df = pd.read_csv(CSV_FILE)

    # Filter based on origin/destination if provided
    if origin:
        df = df[df['origin'].str.lower() == origin.lower()]

    # Convert filtered DataFrame to list of dicts
    results = df.to_dict(orient='records')
    return results
  
def verify_carrier(mc_number: str) -> bool:
    url = (
        f"https://mobile.fmcsa.dot.gov/qc/services/carriers/"
        f"{mc_number}?webKey={WEB_TOKEN}"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                return False

            content = data.get("content")
            if isinstance(content, dict):
                return True
            else:
                return False
        else:
            print(f"Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"FMCSA API error: {e}")
        return False

@router.get("/search_loads")
def get_loads(origin: Optional[str] = None):
    loads = search_loads(origin)
    if not loads:
        raise HTTPException(status_code=404, detail="No loads found")
    return {"loads": loads}
  
@router.get("/verify_carrier")
def api_verify_carrier(mc_number: str):
    eligible = verify_carrier(mc_number)
    return {
        "mc_number": mc_number,
        "eligible": eligible
    }

# Application entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, log_level="info")