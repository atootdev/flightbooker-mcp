from serpapi import GoogleSearch
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from models.flight import Flight, LayOver, FlightSearchParams, FlightSearchResult, FlightSearchResponse

class SerpApi:
    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
    
    async def get_flights(
        self,
        data: FlightSearchParams
    ) -> List[Dict[str, Any]]:
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
            "departure_id": data.departure_id,
            "arrival_id": data.arrival_id,
            "outbound_date": data.departure_date,
            "adults": data.adults,
            "children": data.children,
            "infants_in_seat": data.infants_in_seat,
            "infants_in_lap": data.infants_in_lap,
            "type": data.type,
            "cabin_class": data.cabin_class,
            "stops": data.stops,
            "bags": data.bags,
            "search_location": data.search_location,
            "api_key": self.api_key
        }
        
        if data.return_date:
            params["return_date"] = data.return_date
        if data.max_price:
            params["max_price"] = data.max_price
        
        search = GoogleSearch(params)
        results: Dict[Any, Any] = search.get_dict()
        if results.get("error"):
            raise RuntimeError(f"SerpAPI Error: {results['error']}")
        
        all_flights: List[Dict[str, Any]] = results.get("best_flights", []) + results.get("other_flights", [])
        
        return all_flights
