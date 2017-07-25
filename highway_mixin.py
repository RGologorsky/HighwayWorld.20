# Highway Mixin
# drawing functions and other generally useful functions
from constants import *
from helpers import *

class HighwayMixin(object):

    odd_time = False

    lane_sep_color = WHITE
    lane_color     = GRAY
    
    increment = 3.5 # lane-change
    max_increment = 7

    # STRING/PRINTING functions
    def __str__(self):
        res = "Highway State. \n"
        for car in self.car_list:
            res += ("Lane = %d. Pos = %3d. Speed = %2.1f. ID = %2d. \n" % \
                (car.lane, car.lane_pos, car.speed, car.id))
        return res

    def print_state(self):
        return print(str(self))

    # DRAWING FUNCTIONS

    def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, \
            [x,y,self.lane_width, self.highway_len], 0)

    def draw_sep(self, screen, x, y):
        step_size = int(self.highway_len/20)
        sep_size = int(step_size/2)
        for i in range(0, self.highway_len, step_size):
            curr_y = y + i
            pygame.draw.line(screen, self.lane_sep_color, \
                (x,curr_y), (x, curr_y + sep_size), 2)

    def draw_sep_line(self, screen, x, y):
            pygame.draw.line(screen, self.lane_sep_color, \
                (x,y), (x, y + self.highway_len), 2)


    def draw_highway_state(self, screen, x, y):
        render_multi_line(screen, str(self), x, y)

    def draw_agent_car(self, agent_car, screen, x, y):
        render_multi_line(screen, str(agent_car), x, y)

    def draw_simulator_settings(self, agent_car, screen, x, y):
        simulator_settings = agent_car.print_simulator_settings()
        render_multi_line(screen, simulator_settings, x, y)
    
    def draw_agent_speeds(self, max_speed, curr_speed, screen, loc = (0, 0)):
        (x, y) = loc

        # draw speed limit
        speed_limit = "Speed Limit: %.2f" % max_speed
        curr_speed = "Current Speed: %.2f" % curr_speed
        render_multi_line(screen, speed_limit + "\n" + curr_speed, x, y, text_color = RED)

    def draw(self, screen):
        
        # start at top-left
        curr_x, y = 0, 0
        agent_car = None
        
        # draw lanes
        for i in range(self.num_lanes):
            self.draw_lane(screen, curr_x, y)
            curr_x += self.lane_width
    
        # draw lane seperators
        self.odd_time = not self.odd_time
        start_y = y if self.odd_time else y + self.increment

        curr_x = 0
        for i in range(self.num_lanes):
            self.draw_sep(screen, curr_x, start_y)
            curr_x += self.lane_width
        self.draw_sep_line(screen, curr_x, y)
        self.draw_sep_line(screen, 0, y)

        # draw cars
        for car in self.car_list:
            car.draw(screen);    
            
            if (car.id == 1): 
                agent_car = car  

        # draw agent car features
        x, curr_y  = self.lane_width * self.num_lanes + 100, 10
        if agent_car:
            self.draw_agent_car(agent_car, screen, x, curr_y)
            # draw speed limit and agent car current speed
            self.draw_agent_speeds(agent_car.max_speed, agent_car.speed, screen)
            # draw acceleration, angle, and brake
            curr_y += 200
            self.draw_simulator_settings(agent_car, screen, x, curr_y)

        # draw highway state
        curr_y += 150
        self.draw_highway_state(screen, x, curr_y) 


    
