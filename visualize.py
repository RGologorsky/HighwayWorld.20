from highway_mixin import HighwayMixin
from abstract_car_mixin import AbstractCarMixin

class visualize(HighwayMixin, AbstractCarMixin):
    def __init__(highway_param, highway_time_series):
        self.highway_param = highway_time_series[0]
        self.highway_time_series = highway_time_series

    def draw_cars(self, timestep, car_list):
        pass
    
    def draw_highway(self, timestep):
        highway_snapshot = self.highway_time_series[timstep]
