import os
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp: FastMCP = FastMCP(
    name=os.getenv("MCP_SERVER_NAME", "flight-mcp"),
    version=os.getenv("MCP_SERVER_VERSION", "0.1.0")
)

from apis.serp import SerpApi
api_key = os.getenv("SERP_API_KEY")

if api_key is None:
    raise ValueError("SERP_API_KEY environment variable not set")

serp = SerpApi(api_key=api_key)

async def main():
    # Example usage of get_flights tool
    departure_id = "JFK"
    arrival_id = "LAX"
    departure_date = "2025-10-01"
    adults = 1
    return_date = "2025-10-10"
    type = 1
    travel_class = 1
    children = 0
    infants_in_seat = 0
    infants_in_lap = 0
    stops = 0
    bags = 0
    max_price = None
    search_location = "us"


     # Call the get_flights tool
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
    
    print(data)

if __name__ == "__main__":
    #mcp.run()
    import asyncio
    asyncio.run(main())