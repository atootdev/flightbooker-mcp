from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class CabinClassParam(str, Enum):
    ECONOMY = 1
    PREMIUM_ECONOMY = 2
    BUSINESS = 3
    FIRST = 4
    
    @classmethod
    def from_str(cls, s: str):
        try:
            return cls[s.strip().lower().upper()]
        except KeyError:
            raise ValueError(
                f"Invalid cabin_class '{s}'. Must be one of {[c.name.lower() for c in cls]}."
            )

class FlightTypeParam(str, Enum):
    ROUND_TRIP = 1
    ONE_WAY = 2
    MULTI_CITY = 3
    
    @classmethod
    def from_str(cls, s: str):
        try:
            return cls[s.strip().lower().upper()]
        except KeyError:
            raise ValueError(
                f"Invalid cabin_class '{s}'. Must be one of {[c.name.lower() for c in cls]}."
            )
    
class StopsParam(str, Enum):
    ANY = 0
    NON_STOP = 1
    ONE_STOP = 2
    TWO_STOP = 3
    
    @classmethod
    def from_str(cls, s: str):
        try:
            return cls[s.strip().lower().upper()]
        except KeyError:
            raise ValueError(
                f"Invalid cabin_class '{s}'. Must be one of {[c.name.lower() for c in cls]}."
            )

class CabinClassResult(str, Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"

class FlightTypeResult(str, Enum):
    ROUND_TRIP = "round_trip"
    ONE_WAY = "one_way"
    MULTI_CITY = "multi_city"

class Flight(BaseModel):
    airline: str
    flight_number: str
    departure_airport: str = Field(..., pattern="^[A-Z]{3}$", description="3-letter IATA code")
    arrival_airport: str = Field(..., pattern="^[A-Z]{3}$", description="3-letter IATA code")
    departure_time: str
    arrival_time: str
    duration: str  # e.g., "5h 30m"
    airplane: str
    travel_class: str # "economy", "premium_economy", "business", "first"

class LayOver(BaseModel):
    duration: str  # e.g., "5h 30m"
    airport: str = Field(..., pattern="^[A-Z]{3}$")
    overnight: bool
    
class FlightSearchParams(BaseModel):
    departure_id: str = Field(..., pattern="^[A-Z]{3}$")
    arrival_id: str = Field(..., pattern="^[A-Z]{3}$")
    departure_date: str  # YYYY-MM-DD
    return_date: Optional[str] = None  # YYYY-MM-DD
    adults: int = 1
    children: Optional[int] = 0
    infants_in_seat: Optional[int] = 0
    infants_in_lap: Optional[int] = 0
    type: Optional[int] = 1  # "round_trip", "one_way", "multi_city"
    cabin_class: Optional[int] = 1  # "economy", "premium_economy", "business", "first"
    stops: Optional[int] = 0  # "any", "non_stop", "one_stop", "two_stop"
    bags: Optional[int] = 0
    max_price: Optional[float] = None
    search_location: Optional[str] = "us"
    departure_token: Optional[str] = None # Encoded token for return flights
    booking_token: Optional[str] = None # Encoded token for booking
    
    @field_validator("departure_date", "return_date")
    def validate_date_format(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Date '{v}' is not in 'YYYY-MM-DD' format.")
        return v

class FlightSearchResult(BaseModel):
    flights: List[Flight]
    layover: Optional[List[LayOver]] = None
    total_duration: str  # in hours and minutes (HH MM)
    price: float
    type: str  # "Round trip", "One way", "Multi city"
    departure_token: Optional[str] # Encoded token for return flights
    booking_token: Optional[str] # Encoded token for booking
    
class FlightSearchResponse(BaseModel):
    results: List[FlightSearchResult]