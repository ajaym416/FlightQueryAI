from pydantic import BaseModel
from google import genai
from google.genai import types
from core.config import GEMINI_API_KEY

sys_instruct="""You are an expert SQL assistant specializing in PostgreSQL.
					The database schema is as follows:

					1. Airline Table
					- iata_code (TEXT, PRIMARY KEY) - Unique airline code
					- airline (TEXT) - Name of the airline

					2. Airport Table
					- iata_code (TEXT, PRIMARY KEY) - Unique airport code
					- airport (TEXT) - Name of the airport
					- city (TEXT) - City where the airport is located
					- state (TEXT) - State where the airport is located
					- country (TEXT) - Country of the airport
					- latitude (FLOAT) - Latitude coordinate
					- longitude (FLOAT) - Longitude coordinate

					3. Flight Table
					- id (INTEGER, PRIMARY KEY) - Unique flight ID
					- year (INTEGER) - Flight year
					- month (INTEGER) - Flight month
					- day (INTEGER) - Flight day
					- day_of_week (INTEGER) - Day of the week (1-7)
					- airline_id (TEXT, FOREIGN KEY → airline.iata_code) - Airline operating the flight
					- flight_number (TEXT) - Flight number
					- tail_number (TEXT) - Aircraft tail number
					- origin_airport_id (TEXT, FOREIGN KEY → airport.iata_code) - Departure airport
					- destination_airport_id (TEXT, FOREIGN KEY → airport.iata_code) - Arrival airport
					- scheduled_departure (INTEGER) - Scheduled departure time (HHMM format)
					- departure_time (INTEGER) - Actual departure time (HHMM format)
					- arrival_time (INTEGER) - Actual arrival time (HHMM format)
					- arrival_delay (INTEGER) - Delay in arrival (minutes)
					- distance (INTEGER) - Distance between airports (miles)

					Given this schema, generate a PostgreSQL query for the natural language request by user.
					Make sure the query is valid.
					Expected Output Format: Return the SQL query in JSON format:
					{"sql_query": "GENERATED_POSTGRESQL_QUERY"}
                    If user asks question unrelated to database or generation of PostgreSQL query is not possible return
                    {"sql_query": "Invalid prompt"}
					"""

class JsonOp(BaseModel):
    sql_query:str

class LLMCaller():
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
    
    def generate_sql(self,prompt):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct,
                max_output_tokens=500,
                temperature = 0.2,
                top_p=0.9,
                response_mime_type = "application/json",
                response_schema=JsonOp)
        )
        query: JsonOp = response.parsed
        return query.sql_query