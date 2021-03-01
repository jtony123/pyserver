from flask import Flask
from flask import jsonify
#from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import xml.parsers.expat
from xml.parsers.expat import ParserCreate, ExpatError, errors
import json
import xmltodict


import requests

import board
import digitalio
import busio
from busio import SPI
import adafruit_max31855
import time
from datetime import datetime, timedelta


app = Flask(__name__)
cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
#api = Api(app)

spi_a = SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
spi_b = SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs_a = digitalio.DigitalInOut(board.D5)
cs_b = digitalio.DigitalInOut(board.D6)


sensorA = adafruit_max31855.MAX31855(spi_a, cs_a,)
sensorB = adafruit_max31855.MAX31855(spi_b, cs_b)

@app.route('/', methods=['GET'])
def index():

    data = {"sensorA": str(round(sensorA.temperature, 1)), "sensorB": str(round(sensorB.temperature, 1))}
    return jsonify(data)

@app.route('/weather', methods=['GET'])
def weather():

    x = datetime.now()
    y = x - timedelta(hours=4, minutes=0)
    param1 = y.strftime("%Y-%m-%d"+"T"+"%H:%M")
    z = x + timedelta(hours=24, minutes=0)
    url = 'http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=53.392650;long=-9.271570;from='
    param1 = y.strftime("%Y-%m-%d"+"T"+"%H:%M")
    param2 = z.strftime("%Y-%m-%d"+"T"+"%H:%M")
    fullUrl = url + param1 + ";to=" + param2

    #response.headers["Content-Type"] = "application/json"
    r = requests.get( fullUrl )
    #print (r.status_code)

    # def first_element(tag, attrs):
    #     print ('first element:', tag, attrs)
    # def last_element(tag):
    #     print ('last element:', tag)
    # def character_value(value):
    #     print ('Character value:', repr(value))

    # parser_expat = xml.parsers.expat.ParserCreate()
    # parser_expat.StartElementHandler = first_element
    # parser_expat.EndElementHandler = last_element
    # parser_expat.CharacterDataHandler = character_value
    # try:
    #     parser_expat.Parse(r.content)
    # except ExpatError as err:
    #     print("Error:", errors.messages[err.code])

    obj = xmltodict.parse(r.content, attr_prefix="")

    myj = json.dumps(obj)

    return myj



#if __name__ == "__main__":
#	from waitress import serve
#	serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090)
