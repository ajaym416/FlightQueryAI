# FlightQueryAI - SQL Query Generation for Airline Datasets

**FlightQueryAI** is a system designed to help generate SQL queries based on natural language input for querying airline datasets. The system allows users to input natural language questions, which are processed to generate corresponding SQL queries and fetch relevant data from a PostgreSQL database. The solution also provides a simple frontend powered by HTMX, where users can easily interact with the backend.

## Features
- **Converts natural language queries to SQL queries.**
- **Pagination**: Handles large datasets by using pagination in the results.
- **Frontend**: Simple, interactive frontend using HTMX for real-time query generation and display.
- **Dockerized**: Easily deployable using Docker Compose, which includes the necessary configuration for the backend and PostgreSQL database.
- **Automatic Database Population**: Upon running `docker-compose up --build`, the database will be automatically populated with data from Kaggle.
- **SQLAlchemy + Alembic**: The project uses SQLModel, SQLAlchemy, and Alembic for database creation and migrations.

## Prerequisites
- Docker and Docker Compose
- A `GEMINI_API_KEY` for query generation and/or other external services. https://ai.google.dev/gemini-api/docs/api-key

## Getting Started

### Step 1: Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/ajaym416/FlightQueryAI.git
cd FlightQueryAI
```
### Step 2: Set Up Environment Variables
A sample .env file is included in the repository. Copy it to create your own environment configuration. Update the api key with your own Gemini api key

```bash
cp .env.sample .env
```
### Step 3: Build the Docker Containers
With Docker Compose, you can easily set up the backend and PostgreSQL database. To build the Docker containers, run the following command:

```bash
docker compose up --build
```
Downloading and populating database might take some time.

### Step 4: Populate database

```bash
cd src/api
python3 populate_database.py
```

### Step 5: Interact with the Application
This will start the FastAPI backend, PostgreSQL database, and other required services. The swagger docs will be available at http://localhost:8010/docs, and the frontend will be accessible at http://localhost:8010. Feel free to change the port in docker-compose

###  Example Queries
You can now interact with the application by visiting the frontend in your browser at http://localhost:8010. Use the natural language interface to input queries such as:

- List all flights departing from JFK airport in January 2015.
- show me all data from airlines
- What are the available airports and their locations?
- delete all data from flight where airport is JFK #it will throw an error

# Troubleshooting
- Error: Database connection failure: Ensure that the PostgreSQL credentials in your .env file are correct. If you're running PostgreSQL in Docker, make sure the container is running correctly.
- API Key issues: If you're using an external service for query generation (like Gemini API), ensure the GEMINI_API_KEY is correctly set.
- Database Population: The database is populated automatically from KaggleHub. Ensure that the internet connection is active during the build process for the database population.





