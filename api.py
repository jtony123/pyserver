from flask import Flask
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

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#api = Api(app)

spi = SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31855.MAX31855(spi, cs);

@app.route('/', methods=['GET'])
def index():
	return str(round(sensor.temperature, 1))

@app.route('/weather', methods=['GET'])
def weather():

    #response.headers["Content-Type"] = "application/json"
    r = requests.get('http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=53.392650;long=-9.271570')
    print (r.status_code)

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
