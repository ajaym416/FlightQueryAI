from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Airlines Table
class Airline(SQLModel, table=True):
    iata_code: str = Field(primary_key=True, max_length=3) 
    airline: str

    flights: List["Flight"] = Relationship(back_populates="airline")

# Airports Table
class Airport(SQLModel, table=True):
    iata_code: str = Field(primary_key=True, max_length=3)
    airport: str
    city: str
    state: str
    country: str
    latitude: float
    longitude: float

    origin_flights: List["Flight"] = Relationship(back_populates="origin_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.origin_airport]"})
    destination_flights: List["Flight"] = Relationship(back_populates="destination_airport", sa_relationship_kwargs={"foreign_keys": "[Flight.destination_airport]"})

# Flights Table
class Flight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    year: int
    month: int
    day: int
    day_of_week: int
    airline: str = Field(foreign_key="airline.iata_code")
    flight_number: str
    tail_number: Optional[str] = None
    origin_airport: str = Field(foreign_key="airport.iata_code")
    destination_airport: str = Field(foreign_key="airport.iata_code")
    scheduled_departure: Optional[int] = None
    departure_time: Optional[int] = None
    departure_delay: Optional[int] = None
    taxi_out: Optional[int] = None
    wheels_off: Optional[int] = None
    scheduled_time: Optional[int] = None
    elapsed_time: Optional[int] = None
    air_time: Optional[int] = None
    distance: Optional[int] = None
    wheels_on: Optional[int] = None
    taxi_in: Optional[int] = None
    scheduled_arrival: Optional[int] = None
    arrival_time: Optional[int] = None
    arrival_delay: Optional[int] = None
    diverted: Optional[int] = None
    cancelled: Optional[int] = None
    cancellation_reason: Optional[str] = None
    air_system_delay: Optional[int] = None
    security_delay: Optional[int] = None
    airline_delay: Optional[int] = None
    late_aircraft_delay: Optional[int] = None
    weather_delay: Optional[int] = None

    airline: Airline = Relationship(back_populates="flights")
    origin_airport: Airport = Relationship(back_populates="origin_flights")
    destination_airport: Airport = Relationship(back_populates="destination_flights")
