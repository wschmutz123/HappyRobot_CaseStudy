from fastapi import HTTPException, Query, APIRouter
from dotenv import load_dotenv
import os
import logging
import uvicorn
from typing import Optional, List
import pandas as pd
import requests

# Load environment variables
load_dotenv()

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "..", "Data", "loads.csv")

def search_loads(origin: Optional[str] = None, destination: Optional[str] = None):
    # Read CSV into a DataFrame
    df = pd.read_csv(CSV_FILE)

    # Filter based on origin/destination if provided
    if origin:
        df = df[df['origin'].str.lower() == origin.lower()]
    if destination:
        df = df[df['destination'].str.lower() == destination.lower()]

    # Convert filtered DataFrame to list of dicts
    results = df.to_dict(orient='records')
    return results
  
def verify_carrier(mc_number: str) -> bool:
    url = f"https://safer.fmcsa.dot.gov/query.asp?query_type=queryCarrierSnapshot&query_param=MCNumber&query={mc_number}&displayformat=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(data)
        # Adjust based on actual FMCSA API response structure
        return data.get("eligible_to_work", False)
    except Exception as e:
        print(f"FMCSA API error: {e}")
        return False

def negotiate_rate(listed_rate: float, counter_offers: List[float]) -> float:
    agreed_rate = listed_rate
    for i, offer in enumerate(counter_offers[:3]):
        if offer >= listed_rate * 0.9:
            agreed_rate = offer
        else:
            agreed_rate *= 0.95  # AI makes new offer
    return agreed_rate

@router.get("/search_loads")
def get_loads(origin: Optional[str] = None, destination: Optional[str] = None):
    loads = search_loads(origin, destination)
    if not loads:
        raise HTTPException(status_code=404, detail="No loads found")
    return {"loads": loads}
  
@router.get("/verify_carrier")
def api_verify_carrier(mc_number: str) -> bool:
    eligible = verify_carrier(mc_number)
    return {"mc_number": mc_number, "eligible": eligible}
  
@router.post("/negotiate_rate")
def api_negotiate_rate(listed_rate: float, counter_offers: List[float]):
    agreed_rate = negotiate_rate(listed_rate, counter_offers)
    return {"listed_rate": listed_rate, "counter_offers": counter_offers, "agreed_rate": agreed_rate}
  

@router.post("/find_and_negotiate")
def find_and_negotiate(mc_number: str, origin: Optional[str] = None, destination: Optional[str] = None, counter_offers: Optional[List[float]] = []):
    # 1. Verify carrier
    if not verify_carrier(mc_number):
        raise HTTPException(status_code=403, detail="Carrier not eligible")

    # 2. Search loads
    loads = search_loads(origin, destination)
    if not loads:
        raise HTTPException(status_code=404, detail="No loads found")

    # 3. Negotiate rate for the first load (example)
    first_load = loads[0]
    agreed_rate = negotiate_rate(first_load['loadboard_rate'], counter_offers)

    # Return all relevant info
    return {
        "carrier_mc": mc_number,
        "load": first_load,
        "agreed_rate": agreed_rate
    }

# Application entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, log_level="info")