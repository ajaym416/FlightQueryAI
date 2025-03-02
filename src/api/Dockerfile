FROM python:3.11

WORKDIR /api

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head
RUN python3 ./populate_database.py