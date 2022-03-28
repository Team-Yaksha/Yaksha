from Sensors.BaseSensor import BaseSensor
from seeed_dht import DHT
import time


class AirTemperatureHumiditySensor(BaseSensor):
    def __init__(self):
        BaseSensor.__init__(self)
        
        self.dht_pin = 16
        self.dht_type = '11'
        self.humidity_measurments =[]
        self.temperature_measurments = []
        self.sensor = None
        
    def setup(self): # Sets up the sensor
        try:
            self.sensor = DHT(self.dht_pin, self.dht_type)
            self.init = True
        except Exception as e:
            print("AirTemperatureHumiditySensor: setup: " + str(e))
            self.init = False
            
    def read(self): # Returns the air_humidity and air_temperature
        air_humidity, air_temperature = self._take_readings()
        if  (air_humidity == 0 or air_temperature == 0):
            time.sleep(0.1)
            reH, reT = self._take_readings()
            if (air_humidity == 0):
                air_humidity = reH
            if (air_temperature == 0):
                air_temperature = reT
                
        air_humidity =  self.rolling_average(air_humidity, self.humidity_measurments, self.count)
        air_temperature = self.rolling_average(air_temperature, self.temperature_measurments, self.count)
        return air_humidity, air_temperature
    
    def _take_readings(self): # Reads the sensor and returns the air_humidity and air_temperature
        try:
            if not self.init:
                self.setup()
            for i in range(0, self.count):
                air_humidity, air_temperature = self.sensor.read()
                self.humidity_measurments.append(air_humidity)
                self.temperature_measurments.append(air_temperature)
                i+=1
        except Exception as e:
            print("AirTemperatureHumiditySensor: read: " + str(e))
            self.init = False
            air_humidity, air_temperature = self.null_value, self.null_value
        finally:
            return air_humidity, air_temperature