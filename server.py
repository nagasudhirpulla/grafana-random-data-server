from flask import Flask, request
from dateutil import parser
import datetime as dt

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!!!"


@app.route('/', methods=["POST"])
def query():
    # get the request JSON
    req = request.get_json()
    print(req)

    # get the start and end times
    startTime = parser.parse(req["TimeRange"]["From"])
    endTime = parser.parse(req["TimeRange"]["To"])
    
    # get the payload from json
    # payloadStr = req["JSON"]["payload"]

    # derive the response series name
    seriesName = req["RefID"]
    if "alias" in req["JSON"].keys():
        alias = req["JSON"]["alias"].strip()
        if not len(alias) == 0:
            seriesName = alias

    # generate the response object
    resp = {"frames": [{"columns":[
        {"name": "@timestamp",
         "values": [
            1000*dt.datetime.timestamp(startTime),
            1000*dt.datetime.timestamp(endTime)
            ], "labels": None},
        {"name": seriesName, "values": [5, 10], "labels": None}]}
    ]}
    print(resp)
    return resp


app.run(host="0.0.0.0", port=8080, debug=True)
