import os
import kagglehub
import pandas as pd
from loguru import logger
from app.db import get_session
from app.db.models import Airline, Airport, Flight
import numpy as np

# Download the current version that is 1
logger.info("Downloading Flight delay dataset version 1 from kaggle")
path = kagglehub.dataset_download("usdot/flight-delays/versions/1")

logger.info(f"Dataset downloaded to{path}")

airlines_df = pd.read_csv(os.path.join(path, "airlines.csv"))
airports_df = pd.read_csv(os.path.join(path, "airports.csv"))
flights_df = pd.read_csv(os.path.join(path, "flights.csv"))
# Function to bulk insert DataFrame into database
def bulk_insert(session, model, df):
    objects = [model(**row) for row in df.to_dict(orient="records")]
    session.bulk_save_objects(objects)
    session.commit()


def insert_data(airlines_df, airports_df, flights_df):
    with next(get_session()) as session:
        # Insert Airlines
        logger.info("Inserting data into Airline table")
        airline_objs = [
            Airline(
                iata_code=row["IATA_CODE"],
                airline=row["AIRLINE"]
            )
            for row in airlines_df.to_dict(orient="records")
        ]
        session.bulk_save_objects(airline_objs)
        session.commit()
        logger.info("Inserting data into Airline table Completed")
        
        # Insert Airports
        logger.info("Inserting data into Airports table")
        airport_objs = [
            Airport(
                iata_code=row["IATA_CODE"],
                airport=row["AIRPORT"],
                city=row["CITY"],
                state=row["STATE"],
                country=row["COUNTRY"],
                latitude=row["LATITUDE"],
                longitude=row["LONGITUDE"]
            )
            for row in airports_df.to_dict(orient="records")
        ]
        session.bulk_save_objects(airport_objs)
        session.commit()
        logger.info("Inserting data into Airport table Completed")

        # Insert Flights (use the renamed foreign key columns)
        logger.info("Inserting data into Flight table")
        
        #the flights database is pretty large thus populating chunk by chunk; reduce chunk size as per the memory available
        chunk_size = 50000

        # Total number of rows in flights_df
        num_rows = len(flights_df)
        for start in range(0, num_rows, chunk_size):
            end = start + chunk_size
            chunk_df = flights_df.iloc[start:end]
            chunk_df = chunk_df.replace([np.nan], [None])
            flight_objs = [
                Flight(
                    year=row["YEAR"],
                    month=row["MONTH"],
                    day=row["DAY"],
                    day_of_week=row["DAY_OF_WEEK"],
                    airline_id=row["AIRLINE"],
                    flight_number=row["FLIGHT_NUMBER"],
                    tail_number=row.get("TAIL_NUMBER"),
                    origin_airport_id=row["ORIGIN_AIRPORT"],
                    destination_airport_id=row["DESTINATION_AIRPORT"],
                    scheduled_departure=row.get("SCHEDULED_DEPARTURE"),
                    departure_time=row.get("DEPARTURE_TIME"),
                    departure_delay=row.get("DEPARTURE_DELAY"),
                    taxi_out=row.get("TAXI_OUT"),
                    wheels_off=row.get("WHEELS_OFF"),
                    scheduled_time=row.get("SCHEDULED_TIME"),
                    elapsed_time=row.get("ELAPSED_TIME"),
                    air_time=row.get("AIR_TIME"),
                    distance=row.get("DISTANCE"),
                    wheels_on=row.get("WHEELS_ON"),
                    taxi_in=row.get("TAXI_IN"),
                    scheduled_arrival=row.get("SCHEDULED_ARRIVAL"),
                    arrival_time=row.get("ARRIVAL_TIME"),
                    arrival_delay=row.get("ARRIVAL_DELAY"),
                    diverted=row.get("DIVERTED"),
                    cancelled=row.get("CANCELLED"),
                    cancellation_reason=row.get("CANCELLATION_REASON"),
                    air_system_delay=row.get("AIR_SYSTEM_DELAY"),
                    security_delay=row.get("SECURITY_DELAY"),
                    airline_delay=row.get("AIRLINE_DELAY"),
                    late_aircraft_delay=row.get("LATE_AIRCRAFT_DELAY"),
                    weather_delay=row.get("WEATHER_DELAY")
                )
                for row in chunk_df.to_dict(orient="records")
            ]
            session.bulk_save_objects(flight_objs)
            session.commit()
            logger.info(f"Inserting data into Flight table{end} / {num_rows}")

        logger.info("Inserting data into Flight table completed")
    # with next(get_session()) as session:
    #     # Insert airlines
    #     logger.info("Inserting data into Airline table")
    #     bulk_insert(
    #         session,
    #         Airline,
    #         airlines_df.rename(
    #             columns={"IATA_CODE": "iata_code", "AIRLINE": "airline"}
    #         ),
    #     )
    #     logger.info("Inserting data into Airline table Completed")
    #     # Insert airports
    #     logger.info("Inserting data into Airport table")
    #     bulk_insert(
    #         session,
    #         Airport,
    #         airports_df.rename(
    #             columns={
    #                 "IATA_CODE": "iata_code",
    #                 "AIRPORT": "airport",
    #                 "CITY": "city",
    #                 "STATE": "state",
    #                 "COUNTRY": "country",
    #                 "LATITUDE": "latitude",
    #                 "LONGITUDE": "longitude",
    #             }
    #         ),
    #     )
    #     logger.info("Inserting data into Airport table Completed")

    #     # Insert flights
    #     logger.info("Inserting data into Flight table")
    #     bulk_insert(
    #         session,
    #         Flight,
    #         flights_df.rename(
    #             columns={
    #                 "YEAR": "year",
    #                 "MONTH": "month",
    #                 "DAY": "day",
    #                 "DAY_OF_WEEK": "day_of_week",
    #                 "AIRLINE": "airline",
    #                 "FLIGHT_NUMBER": "flight_number",
    #                 "TAIL_NUMBER": "tail_number",
    #                 "ORIGIN_AIRPORT": "origin_airport_id",
    #                 "DESTINATION_AIRPORT": "destination_airport_id",
    #                 "SCHEDULED_DEPARTURE": "scheduled_departure",
    #                 "DEPARTURE_TIME": "departure_time",
    #                 "DEPARTURE_DELAY": "departure_delay",
    #                 "TAXI_OUT": "taxi_out",
    #                 "WHEELS_OFF": "wheels_off",
    #                 "SCHEDULED_TIME": "scheduled_time",
    #                 "ELAPSED_TIME": "elapsed_time",
    #                 "AIR_TIME": "air_time",
    #                 "DISTANCE": "distance",
    #                 "WHEELS_ON": "wheels_on",
    #                 "TAXI_IN": "taxi_in",
    #                 "SCHEDULED_ARRIVAL": "scheduled_arrival",
    #                 "ARRIVAL_TIME": "arrival_time",
    #                 "ARRIVAL_DELAY": "arrival_delay",
    #                 "DIVERTED": "diverted",
    #                 "CANCELLED": "cancelled",
    #                 "CANCELLATION_REASON": "cancellation_reason",
    #                 "AIR_SYSTEM_DELAY": "air_system_delay",
    #                 "SECURITY_DELAY": "security_delay",
    #                 "AIRLINE_DELAY": "airline_delay",
    #                 "LATE_AIRCRAFT_DELAY": "late_aircraft_delay",
    #                 "WEATHER_DELAY": "weather_delay",
    #             }
    #         ),
    #     )
    #     logger.info("Inserting data into Flight table completed")

if __name__ =="__main__":
    insert_data(airlines_df, airports_df, flights_df)