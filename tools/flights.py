import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from models.flight import CabinClass, FlightType, Stops, Flight
from utils.validate_date import validate_date
from apis.serp import SerpApi

# Get the MCP instance from main server
from server import mcp

# Initialize SerpApi with the API key from environment variables
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("SERP_API_KEY")

if api_key is None:
    raise ValueError("SERP_API_KEY environment variable not set")

serp = SerpApi(api_key=api_key)

@mcp.tool()
async def get_flights(
    departure_id: str,
    arrival_id: str,
    departure_date: str,
    adults: int,
    return_date: Optional[str] = None,
    flight_type: Optional[str] = "round_trip",
    cabin_class: Optional[str] = "economy",
    children: Optional[int] = 0,
    infants_in_seat: Optional[int] = 0,
    infants_in_lap: Optional[int] = 0,
    no_stops: Optional[str] = "any",
    bags: Optional[int] = 0,
    max_price: Optional[float] = None,
    search_location: Optional[str] = "us",
) -> List[Dict[str, Any]]:
    """
    Fetch flight prices based on the provided criteria.

    Args:
        departure_id (str): IATA code of the departure airport.
        arrival_id (str): IATA code of the arrival airport.
        departure_date (str): Departure date in YYYY-MM-DD format.
        adults (int): Number of adult passengers.
        return_date (Optional[str], optional): Return date in YYYY-MM-DD format. Defaults to None.
        flight_type (Optional[str], optional): Type of flight: "round_trip", "one_way", "multi_city". Defaults to "round_trip".
        cabin_class (Optional[str], optional): Cabin class: "economy", "premium_economy", "business", "first". Defaults to "economy".
        children (Optional[int], optional): Number of child passengers. Defaults to 0.
        infants_in_seat (Optional[int], optional): Number of infants in seat. Defaults to 0.
        infants_in_lap (Optional[int], optional): Number of infants in lap. Defaults to 0.
        no_stops (Optional[str], optional): Number of stops: "any", "nonstop", "onestop", "twostop". Defaults to "any".
        bags (Optional[int], optional): Number of bags. Defaults to 0.
        max_price (Optional[float], optional): Maximum price filter. Defaults to unlimited.
        search_location (Optional[str], optional): Search location (e.g., "us", "uk"). Defaults to "us". 
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing flight details.
    """
    # Validate date formats
    validate_date(departure_date, "departure_date")
    if return_date is not None:
        validate_date(return_date, "return_date")
    
    # Convert enums
    flight_enum = None
    type = 1  # default to round-trip
    
    if flight_type is not None:
        flight_enum = FlightType.from_str(flight_type)
        type = flight_enum.value
    
    cabin_enum = None
    travel_class = 1  # default to economy
    
    if cabin_class is not None:
        cabin_enum = CabinClass.from_str(cabin_class)
        travel_class = cabin_enum.value
    
    stops_enum = None
    stops = 0  # default to any
    if no_stops is not None:
        stops_enum = Stops.from_str(no_stops)
        stops = stops_enum.value
    
    try:
        # Call the SerpApi to get flight data
        data = await serp.get_flights(
            departure_id=departure_id,
            arrival_id=arrival_id,
            departure_date=departure_date,
            adults=adults,
            return_date=return_date,
            type=type,
            travel_class=travel_class,
            children=children,
            infants_in_seat=infants_in_seat,
            infants_in_lap=infants_in_lap,
            stops=stops,
            bags=bags,
            max_price=max_price,
            search_location=search_location
        )
        
        best_flights = data.get("best_flights", [])
        flights = 
    
    return {
        "success": True,
        "search_id": f"SRCH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "results": data.get("flights", [])
    }