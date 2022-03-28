from datetime import datetime
from Sensors.SoilTemperatureSensor import SoilTemperatureSensor
from Sensors.SoilMoistureSensor import SoilMoistureSensor
from Sensors.AirTemperatureHumiditySensor import AirTemperatureHumiditySensor
from Sensors.SunlightSensor import SunlightSensor


class SensorPoller:
    def __init__(self):
        self.null_value = 0
        self.data = {}
        
        self.soil_temperature_sensor = SoilTemperatureSensor()
        self.soil_moisture_sensor = SoilMoistureSensor()
        self.air_temperature_humidity_sensor = AirTemperatureHumiditySensor()
        self.sunlight_sensor = SunlightSensor()

        
    def poll_sensors(self):
        print("Polling Sensors")
        self.set_date_time()
        self.set_soil_temperature()
        self.set_soil_moisture()
        self.set_air_temperature_humidity()
        self.set_sunlight()
        return self.data

    def set_date_time(self):
        date_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        self.data.update({'date_time': date_time})

# ------------------ Capture Data ----------------#
    def set_soil_temperature(self):
        self.data.update({'soil_temperature': self.soil_temperature_sensor.read()})

    def set_soil_moisture(self):
        self.data.update({'soil_moisture': self.soil_moisture_sensor.read()})

    def set_air_temperature_humidity(self):
        air_temperature, humidity = self.air_temperature_humidity_sensor.read()
        self.data.update({'air_temperature': air_temperature})
        self.data.update({'humidity': humidity})

    def set_sunlight(self):
        sunlight_visble, sunlight_uv, sunlight_ir = self.sunlight_sensor.read()
        self.data.update({'sunlight_visible': sunlight_visble}) # Visibile light
        self.data.update({'sunlight_uv': sunlight_uv})  # UV light
        self.data.update({'sunlight_ir': sunlight_ir})  # IR light

# ------------------ Send Data ----------------#            
    def send_data(self):
        return self.data
