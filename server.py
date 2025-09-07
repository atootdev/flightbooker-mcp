import os
from dotenv import load_dotenv
from fastmcp import FastMCP

import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from models.flight import (
    CabinClassParam, FlightTypeParam, StopsParam, LayOver, FlightSearchParams, 
    Flight, FlightSearchResult
    )
from utils.validate_date import validate_date
from apis.serp import SerpApi


# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp: FastMCP = FastMCP(
    name=os.getenv("MCP_SERVER_NAME", "flight-mcp"),
    version=os.getenv("MCP_SERVER_VERSION", "0.1.0")
)

api_key: str | None = os.getenv("SERP_API_KEY")

if api_key is None:
    raise ValueError("SERP_API_KEY environment variable not set")

serp = SerpApi(api_key=api_key)

def _transform_duration(duration: int) -> str:
        """Convert duration in minutes to "HH MM" format."""
        hours: int = duration // 60
        minutes: int = duration % 60
        return f"{hours}H {minutes}M"
    
def _transform_travel_class(cabin_class: str) -> str:
    """Transform cabin class string to match expected format."""
    cabin_class = cabin_class.strip().lower()
    return re.sub(r"\s+", "_", cabin_class)
        
def _transform_flight_data(flight_data: Dict[str, Any]) -> FlightSearchResult:
    """
    Transform the raw flight data from SerpAPI into a structured format.

    Args:
        flight_data (Dict[str, Any]): Raw flight data from SerpAPI.

    Returns:
        FlightSearchResult: Transformed flight data from SerpAPI.
    """
    
    flights: List[Flight] = []
    layovers: List[LayOver] = []
    
    for flight_info in flight_data.get("flights", []):
        flight: Flight = Flight(
            airline = flight_info.get("airline", ""),
            flight_number = flight_info.get("flight_number", ""),
            departure_airport = flight_info.get("departure_airport", {}).get("id", ""),
            arrival_airport = flight_info.get("arrival_airport", {}).get("id", ""),
            departure_time = flight_info.get("departure_airport", {}).get("time", ""),
            arrival_time = flight_info.get("arrival_airport", {}).get("time", ""),
            duration = _transform_duration(flight_info.get("duration", 0)),
            airplane = flight_info.get("airplane", ""),
            travel_class = _transform_travel_class(flight_info.get("travel_class", ""))
        )
        flights.append(flight)
    
    for layover_info in flight_data.get("layovers", []):
        layover: LayOver = LayOver(
            duration = _transform_duration(layover_info.get("duration", 0)),
            airport = layover_info.get("id", ""),
            overnight = layover_info.get("overnight", False)
        )
        layovers.append(layover)
    
    return FlightSearchResult(
        flights = flights,
        layover = layovers if layovers else None,
        total_duration = _transform_duration(flight_data.get("total_duration", 0)),
        price = flight_data.get("price", 0),
        type = flight_data.get("type", ""),
        departure_token = flight_data.get("departure_token", None),
        booking_token = flight_data.get("booking_token", None),
    )

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
    departure_token: Optional[str] = None,
    booking_token: Optional[str] = None
) -> Dict[str, Any]:
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
        departure_token (Optional[str], optional): Encoded token for return flights. Defaults to None.
        booking_token (Optional[str], optional): Encoded token for booking. Defaults to None.
        
    Returns:
        Dict[str, Any]: Dictionary containing flight details.
    """
    # Validate date formats
    validate_date(departure_date, "departure_date")
    
    if return_date is not None:
        validate_date(return_date, "return_date")
    
    # Convert enums
    flight_enum = None
    type = 1  # default to round-trip
    
    if flight_type is not None:
        flight_enum = FlightTypeParam.from_str(flight_type)
        type = flight_enum.value
    
    cabin_enum = None
    travel_class = 1  # default to economy
    
    if cabin_class is not None:
        cabin_enum = CabinClassParam.from_str(cabin_class)
        travel_class = cabin_enum.value
    
    stops_enum = None
    stops = 0  # default to any
    if no_stops is not None:
        stops_enum = StopsParam.from_str(no_stops)
        stops = stops_enum.value
    
    params = FlightSearchParams(
        departure_id=departure_id,
        arrival_id=arrival_id,
        departure_date=departure_date,
        return_date=return_date,
        adults=adults,
        children=children,
        infants_in_seat=infants_in_seat,
        infants_in_lap=infants_in_lap,
        type=type,
        cabin_class=travel_class,
        stops=stops,
        bags=bags,
        max_price=max_price,
        search_location=search_location,
        departure_token=departure_token,
        booking_token=booking_token
    )
    
    try:
        # Call the SerpApi to get flight data
        flight_response: List[Dict[str, Any]] = await serp.get_flights(data=params)
        
        flights: List[FlightSearchResult] = [
            _transform_flight_data(f) for f in flight_response
        ]
    
        return {
            "success": True,
            "search_id": f"SRCH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "flights": [f.model_dump() for f in flights[:10]],
            "total_flights": len(flights),
            "search_criteria": params.model_dump()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

@mcp.prompt()
async def find_best_flight(
    travel_details: str,
    preferences: str
) -> str:
    """
    AI-assisted flight search based on natural language preferences.
    
    Args:
        travel_details: Natural language description of travel plans
        preferences: User preferences for the flight
    
    Returns:
        Structured prompt for optimal flight search
    """
    return f"""Based on the travel details: "{travel_details}" and preferences: "{preferences}", 
    I'll help you find the best flight options. 

    To search effectively, I'll need to:
    1. Extract origin and destination cities
    2. Identify travel dates
    3. Determine number of passengers
    4. Understand your priorities (price, time, airline preference)
    
    Let me search for flights that match your criteria..."""

import tools.flights  # Ensure the flights tool is imported to register it

if __name__ == "__main__":
    # Run the server
    mcp.run()