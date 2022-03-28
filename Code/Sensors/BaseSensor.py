class BaseSensor():
    def __init__(self):
        self.null_value = 0
        self.sensor  = None
        self.init = False
        self.count = 10
        self.measurments = []
        self.upper_reasonable_bound = 200
        self.lower_reasonable_bound = 0
        
    def setup(self):
        self.sensor = None
        
    def read(self):
        return None
    
    def average(self, measurments):
        if len(measurments) != 0:
            return sum(measurments) / len(measurments)
        else:
            return self.null_value
        
    def rolling_average(self, measurment, measurments, size):
        if measurment == None:
            return None
        if self.lower_reasonable_bound  < measurment < self.upper_reasonable_bound:
            while len(measurments) >= size:
                measurments.pop(0)
            measurments.append(measurment)
        return self.average(measurments)
    
    def mapNum(self, val, old_Max, old_Min, new_Max, new_Min):
        try:
            old_range = float(old_Max - old_Min)
            new_Range = float(new_Max - new_Min)
            new_value = float(((val - old_Min) * new_Range) / old_range) + new_Min
            return new_value
        except Exception:
            return val
                