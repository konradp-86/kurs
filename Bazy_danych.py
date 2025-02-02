import csv
import sqlite3
import requests
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db')
Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    name = Column(String)
    country = Column(String)
    state = Column(String)

class Measure(Base):
    __tablename__ = 'measures'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(String)
    precip = Column(Float)
    tobs = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def download_csv_from_github(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.text

stations_csv_url = 'https://raw.githubusercontent.com/konradp-86/kurs/main/clean_stations.csv'
stations_csv_content = download_csv_from_github(stations_csv_url)

measures_csv_url = 'https://raw.githubusercontent.com/konradp-86/kurs/main/clean_measure.csv'
measures_csv_content = download_csv_from_github(measures_csv_url)

stations_reader = csv.DictReader(stations_csv_content.splitlines())
for row in stations_reader:
    station = Station(
        station=row['station'],
        latitude=float(row['latitude']),
        longitude=float(row['longitude']),
        elevation=float(row['elevation']),
        name=row['name'],
        country=row['country'],
        state=row['state']
    )
    session.add(station)


measures_reader = csv.DictReader(measures_csv_content.splitlines())
for row in measures_reader:
    measure = Measure(
        station=row['station'],
        date=row['date'],
        precip=float(row['precip']),
        tobs=float(row['tobs'])
    )
    session.add(measure)
  
session.commit()

conn = sqlite3.connect('example.db')
result = conn.execute("SELECT * FROM stations LIMIT 5").fetchall()

print("Wyświetlenie pierwszych 5 stacji:")
for row in result:
    print(row)

conn.close()
session.close()
print("Dane zostały pobrane i zapisane do bazy danych SQLite.")
