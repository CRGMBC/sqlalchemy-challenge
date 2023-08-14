#import
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
#engine = create_engine("sqlite:///c:/Users/carol/Desktop/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)


# Define Home Page & list all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>Dictionary by date of precipitation<br/>"
        f"/api/v1.0/stations<br/>A list of stations<br/>"
        f"/api/v1.0/tobs<br/>Temperature observations for the previous year<br/>"
        f"/api/v1.0/<start_date_only><br/>Min, Average & Max tobs - enter start date at the end of the URL (between 23 Aug 2016 and 23 Aug 2017 inclusive)<br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>Min,Average & Max temperature observations - enter start date,fwd slash, then enter end date using format yyyy-mm-dd (between 23 Aug 2016 and 23 Aug 2017 inclusive)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query the meaasurement data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    # Create a dictionary by date of precipitation
    precipitation_list = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)
   
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query to get stations
    stations = session.query(Station.station)

    session.close()

    #create a list of all stations
    station_list = []
    for station in stations:
        station_dict = {}
        station_dict['station'] = station.station
        station_list.append(station_dict)

    # Return a JSON list of stations from the dataset
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs ():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    temperature_data = session.query(Measurement.date,Measurement.tobs)\
        .filter(Station.station == Measurement.station)\
        .filter(Measurement.date >= '2016-08-23')\
        .filter(Station.station == 'USC00519281')\
        .order_by(Measurement.date.desc()).all()

    session.close()

    #Return a JSON list of temperature observations for the previous year
    tobs_list = []
    for date, tobs in temperature_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)

    # Return a JSON list of tobs from the dataset
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date_only>")
def StartDate(start_date_only):
   # Create our session (link) from Python to the DB
    session = Session(engine) 

    #query for a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date_only).group_by(Measurement.date).all()

    session.close()

    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature by start date
    start_list = []
    for date,tmin,tavg,tmax in start_results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = tmin
        start_dict['TAVG'] = tavg
        start_dict['TMAX'] = tmax
        start_list.append(start_dict)

    # Return a JSON list of start date data from the dataset
    return jsonify(start_list)   


@app.route("/api/v1.0/<start_date>/<end_date>")
def StartEndDate(start_date,end_date):
   # Create our session (link) from Python to the DB
    session = Session(engine) 

    #query for a specified start, calculate TMIN, TAVG, and TMAX for all the dates from the start date to the end date, inclusive.
    start_end_results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()

    session.close()

    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature by start date
    startend_list = []
    for date,tmin,tavg,tmax in start_end_results:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = tmin
        startend_dict['TAVG'] = tavg
        startend_dict['TMAX'] = tmax
        startend_list.append(startend_dict)

    # Return a JSON list of start & end date data from the dataset
    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)

