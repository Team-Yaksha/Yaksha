from Sensors.BaseSensor import BaseSensor
from seeed_si114x import grove_si114x


class SunlightSensor(BaseSensor):
    def __init__(self):
        BaseSensor.__init__(self)
        self.sensor = None
        self.init = False
        self.setup()
        
    def setup(self):
        try:
            self.sensor = grove_si114x()
            self.init = True
        except Exception as e:
            print("SunlightSensor.setup: " + str(e))
            self.init = False
            
    def get_read(self):
        try:
            if not self.init:
                self.setup()
            sunlight_visible = self.sensor.ReadVisible()
            for i in range(0, self.count):
                sunlight_uv = self.sensor() / 100
                self.measurments.append(sunlight_uv)
            sunlight_uv =  self.rolling_average(sunlight_uv, self.measusurments, 10)
            sunlight_ir = self.sensor.ReadIR()
        except Exception as e:
            print("SunlightSensor.read: " + str(e))
            sunlight_visible = self.null_value
            sunlight_uv = self.null_value
            sunlight_ir = self.null_value
        finally:
            return (sunlight_visible, sunlight_uv, sunlight_ir)