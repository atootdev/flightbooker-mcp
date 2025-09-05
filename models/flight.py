from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class CabinClass(str, Enum):
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

class FlightType(str, Enum):
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
    
class Stops(str, Enum):
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
    
class Flight(BaseModel):
    flight_id: str
    airline: str
    flight_number: str
    origin: str = Field(..., pattern="^[A-Z]{3}$")
    destination: str = Field(..., pattern="^[A-Z]{3}$")
    departure: datetime
    arrival: datetime
    duration: str  # e.g., "5h 30m"
    aircraft: str
    price: float
