import csv
import sqlite3
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

with open('clean_stations.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
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

with open('clean_measure.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
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
for row in result:
    print(row)

conn.close()
session.close()
