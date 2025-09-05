import os
from serpapi import GoogleSearch
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SERP_API_KEY")

class SerpApi:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
    
    async def get_flights(
        self,
        departure_id: str,
        arrival_id: str,
        departure_date: str,
        adults: int,
        return_date: Optional[str] = None,
        type: Optional[int] = 1,
        travel_class: Optional[int] = 1,
        children: Optional[int] = 0,
        infants_in_seat: Optional[int] = 0,
        infants_in_lap: Optional[int] = 0,
        stops: Optional[int] = 0,
        bags: Optional[int] = 0,
        max_price: Optional[float] = None,
        search_location: Optional[str] = "us",
    ) -> Dict[str, Any]:
        """
        Get flights from Google Flights via SerpAPI.

        Args:
            departure_id (str): IATA code of the departure airport.
            arrival_id (str): IATA code of the arrival airport.
            departure_date (str): Departure date in YYYY-MM-DD format.
            adults (int): Number of adult passengers.
            return_date (Optional[str], optional): Return date in YYYY-MM-DD format. Defaults to None.
            type (Optional[int], optional): _description_. Type of flight: 1 for round-trip, 2 for one-way, 3 for multi-city. Defaults to 1.
            travel_class (Optional[int], optional): _description_. Type of cabin class: 1 for economy, 2 for premium economy, 3 for business, 4 for first. Defaults to 1.
            children (Optional[int], optional): Number of child passengers. Defaults to 0.
            infants_in_seat (Optional[int], optional): Number of infants in seat. Defaults to 0.
            infants_in_lap (Optional[int], optional): Number of infants in lap. Defaults to 0.
            stops (Optional[int], optional): Number of stops: 0 for any, 1 for non-stop, 2 for one-stop or less, 3 for two-stops or less. Defaults to 0.
            bags (Optional[int], optional): Number of bags. Defaults to 0.
            max_price (Optional[float], optional): Maximum price filter. Defaults to unlimited.
            search_location (Optional[str], optional): Search location (e.g., "us", "uk"). Defaults to "us".

        Returns:
            Dict[str, Any]: Dictionary containing search results with outbound and return flights
        """
        
        params: Dict[str, Any] = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": departure_date,
            "adults": adults,
            "type": type,
            "travel_class": travel_class,
            "children": children,
            "infants_in_seat": infants_in_seat,
            "infants_in_lap": infants_in_lap,
            "stops": stops,
            "bags": bags,
            "gl": search_location,
            "api_key": self.api_key
        }
        
        if return_date:
            params["return_date"] = return_date
        if max_price:
            params["max_price"] = max_price
        
        search = GoogleSearch(params)
        results = search.get_dict()
        return results