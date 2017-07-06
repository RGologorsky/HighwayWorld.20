# Highway Mixin
# drawing functions and other generally useful functions
from constants import *
from drawing_helpers import *

class HighwayMixin(object):

    lane_sep_color = WHITE
    lane_color     = GRAY
    
    lane_height = 76 # little more than Car.height

    # STRING/PRINTING functions
    def __str__(self):
        res = "Highway State. \n"
        for idx in range(self.num_states):
            state = self.idx_to_state(idx)
            if state != (-1, -1):
                lane, lane_pos = self.idx_to_pos(idx)
                res += ("Lane = %d. Pos = %3d. Speed = %2.1f. ID = %2d. \n" % \
                    (lane, lane_pos, state[1], state[0]))
        return res

    def print_state(self):
        return print(str(self))


    # DRAWING FUNCTIONS

    def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, [x,y,self.highway_len,self.lane_height], 0)

    def draw_sep(self, screen, x, y):
        pygame.draw.line(screen, self.lane_sep_color, (x,y), (x + self.highway_len, y), 1)


    def draw_highway_state(self, screen, x, y):
        render_multi_line(screen, str(self), x, y)

    def draw_agent_car(self, agent_car, screen, x, y):
        render_multi_line(screen, str(agent_car), x, y)

    def draw_simulator_settings(self, agent_car, screen, x, y):
        simulator_settings = agent_car.print_simulator_settings()
        render_multi_line(screen, simulator_settings, x, y)
        
    def draw(self, screen):
        # start at top-left
        x, curr_y = 0, 0
        agent_car = None
        
        # draw lanes
        for i in range(self.num_lanes):
            self.draw_lane(screen, x, curr_y)
            curr_y += self.lane_height
    
        # draw lane seperators
        curr_y = 0
        for i in range(self.num_lanes):
            self.draw_sep(screen, x, curr_y)
            curr_y += self.lane_height
        self.draw_sep(screen, x, curr_y)

        # draw cars
        for car in self.car_list:
            car.draw(screen);    
            
            if (car.id == 1): 
                agent_car = car  

        # draw agent car features
        x, curr_y  = 10, curr_y + 10
        if agent_car:
            self.draw_agent_car(agent_car, screen, x, curr_y)

            # draw acceleration, angle, and brake
            x += 600
            self.draw_simulator_settings(agent_car, screen, x, curr_y)

        # draw highway state
        x = screen_width - 400
        self.draw_highway_state(screen, x, curr_y) 
