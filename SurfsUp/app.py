# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from sqlalchemy.sql import text

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

# Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    """List all available api routes."""
    return(
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Starting from the most recent data point in the database. 
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    previous_year = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')-dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    score = session.query(Measurement.date, Measurement.prcp). filter(Measurement.date >= previous_year).all()
    
    session.close()

    # Define Dictionary to return
    dict = {}

    # Convert rows returned from the query to dictionary
    for row in score:
        dict[row.date] = row.prcp

    # Return the dictionary after converting it to json.
    return jsonify(dict)

@app.route('/api/v1.0/stations')
def stations():
    rows = session.query(Station.station).all()

    list = []
    for row in rows:
        list.append(row.station)

    return jsonify(list)

@app.route('/api/v1.0/tobs')
def tobs():
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Starting from the most recent data point in the database. 
    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    previous_year = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')-dt.timedelta(days=366)

    # finding most active station
    mostactive_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
        .filter(Measurement.date >= previous_year).all()
    list_of_temp = []
    for station in mostactive_station:
        list_of_temp.append(station.tobs)

    return jsonify(list_of_temp)

@app.route('/api/v1.0/<start>')
def compute_with_start(start):
    
    # Fetch Min, Avg and Max temprature for measurements greater than or equal to start date passed in the request
    rows = session.query(func.min(Measurement.tobs).label('TMIN'), func.avg(Measurement.tobs).label('TAVG'), func.max(Measurement.tobs).label('TMAX'))\
        .filter(Measurement.date >= start).all()

    # Since returned number of rows is one, we can just access the row list as rows[0]
    return jsonify(rows[0].TMIN, rows[0].TAVG, rows[0].TAVG)

@app.route('/api/v1.0/<start>/<end>')
def compute_with_start_and_end(start, end):

    # Fetch Min, Avg and Max temprature for measurements greater than or equal to start date and less than or equal to end date passed in the request
    rows = session.query(func.min(Measurement.tobs).label('TMIN'), func.avg(Measurement.tobs).label('TAVG'), func.max(Measurement.tobs).label('TMAX'))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Since returned number of rows is one, we can just access the row list as rows[0]
    return jsonify(rows[0].TMIN, rows[0].TAVG, rows[0].TAVG)

if __name__ == "__main__":
    app.run(debug=True)