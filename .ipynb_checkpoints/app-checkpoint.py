import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

inspector = inspect(engine)

conn = engine.connect()

Base = automap_base()
# reflect an existing database into a new model
Base.prepare(engine, reflect=True)
# reflect the tables

# Save references to each table
measurement = Base.classes.measurement

station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Welcome():
    """Hawaii Climate Analysis"""

    return (f"Hawaii Climate Analysis<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    """Rain Observation for Last 365"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Calculate the date one year from the last date in data set.
    one_year_from_max = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year_from_max
    # Perform a query to retrieve the data and precipitation scores
    percipitation_results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_from_max).all()
    percipitation_results
    return jsonify(percipitation_results)


@app.route("/api/v1.0/stations")
def Stations1():
    """List of Stations"""
    dict_station = {}
    for x in engine.execute('SELECT * FROM station').fetchall():
        dict_station[x[0]]= x[1]
    return dict_station
    
@app.route("/api/v1.0/tobs")
def tobs():
    """Most Active Station for the Last Year"""
    one_year_from_max = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year_from_max
    
    active_tobs_365 = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_from_max, measurement.station == 'USC00519281').all()
    return jsonify(active_tobs_365)



if __name__ == "__main__":
    app.run(debug=True)


