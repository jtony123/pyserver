from flask import Flask
#from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

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
	return str(sensor.temperature)


#if __name__ == "__main__":
#	from waitress import serve
#	serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
