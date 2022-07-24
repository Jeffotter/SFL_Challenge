FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev sqlite3

RUN apt-get install -y libpq-dev 
RUN apt-get update 
RUN pip install --upgrade pip

WORKDIR /
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . .
EXPOSE 5000
CMD ["python3", "/ETL.py"]