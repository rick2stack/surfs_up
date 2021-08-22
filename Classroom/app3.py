import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#__name__ is a variable code name, if we wanted to import another app1.py file
# the __name__ to import that py file will be "app1"
app = Flask(__name__)

#import app

#print("example __name__ = %s", __name__)

#if __name__ == "__main__":
    #print("example is being run directly.")
#else:
    #print("example is being imported")

#The "/" just means root folder (or the folder that this file is in)
#the api/vi.0/ are routes
# the naming 
@app.route('/')

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:\n
    /api/v1.0/precipitation \n
    /api/v1.0/stations \n
    /api/v1.0/tobs \n
    /api/v1.0/temp/start/end \n
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#set the start and end paramters to none for now
# but if you want to add a start and end date
# you will have to change the app route 
#/api/v1.0/temp/2017-06-01/2017-06-30 or 
#@app.route("/api/v1.0/temp/<start>")
#@app.route("/api/v1.0/temp/<start>/<end>")
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # the * means that there will be multiple results 
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)





