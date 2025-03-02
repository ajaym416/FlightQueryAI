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
					- scheduled_departure (INTEGER) - Scheduled departure time 
					- departure_time (INTEGER) - Actual departure time 
					- departure_delay (INTEGER) - Delay in arrival (minutes)
					- taxi_out (INTEGER) - taxi out time
					- scheduled_time (INTEGER)
					- elapsed_time (INTEGER)
					- air_time (INTEGER)
					- distance (INTEGER)
					- wheels_on (INTEGER)
					- taxi_in (INTEGER)
					- scheduled_arrival (INTEGER)
					- arrival_time (INTEGER) - Actual arrival time
					- arrival_delay (INTEGER) - Delay in arrival (minutes)
					- diverted (INTEGER)
					- cancelled (INTEGER)
					- cancellation_reason (TEXT)
					- air_system_delay (INTEGER)
					- security_delay (INTEGER)
					- airline_delay (INTEGER)
					- late_aircraft_delay (INTEGER)
					- weather_delay (INTEGER)

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
                # Lower values reduce randomness and ensure deterministic output, which is crucial for SQL queries that must be syntactically and logically correct.
                top_p=0.9,
                # allows the model to generate complete, natural SQL queries while still prioritizing the most likely outputs
                response_mime_type = "application/json",
                response_schema=JsonOp)
        )
        query: JsonOp = response.parsed
        return query.sql_query