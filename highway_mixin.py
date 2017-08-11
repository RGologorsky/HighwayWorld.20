# Highway Mixin
# drawing functions and other generally useful functions
from constants import *
from helpers import *

class HighwayMixin(object):

    # DRAWING FUNCTIONS

    def draw_road(self, screen, x, y):
        highway_width = self.lane_width * self.num_lanes
        pygame.draw.rect(screen, self.road_color, \
            [x,y,highway_width, self.highway_len], 0)

    def draw_dashed_lane(self, screen, x, y):
        # dash_len = length of dash, 
        # gap_len = length of the gap between dash starts

        gap_len  = int(self.highway_len/20)
        dash_len = int(gap_len/2)
        
        for i in range(0, self.highway_len, gap_len):
            curr_y = y + i
            pygame.draw.line(screen, self.lane_color, \
                (x,curr_y), (x, curr_y + dash_len), 2)

    def draw_solid_lane(self, screen, x, y):
            pygame.draw.line(screen, self.lane_color, \
                (x,y), (x, y + self.highway_len), 2)

    # TEXT DRAWING FUNCTIONS (DRAWS STATE/FEATURES onto GAME WINDOW)
    def draw_highway_state(self, screen, x, y):
        render_multi_line(screen, str(self), x, y)


    def draw_agent_car(self, agent_car, screen, x, y):
        render_multi_line(screen, str(agent_car), x, y)

    # DRAWS CURRENT INPUTS to the DRIVING SIMULATOR
    def draw_simulator_inputs(self, agent_car, screen, x, y):
        simulator_inputs = agent_car.print_simulator_settings()
        render_multi_line(screen, simulator_inputs, x, y)
    
    # DRAWS AGENT CURRENT SPEED AND SPEED LIMIT
    def draw_agent_speeds(self, max_speed, curr_speed, screen, loc = (0, 0)):
        (x, y) = loc

        # draw speed limit
        speed_limit = "Speed Limit: %.2f" % max_speed
        curr_speed = "Current Speed: %.2f" % curr_speed
        render_multi_line(screen, speed_limit + "\n" + curr_speed, x, y, text_color = RED)

    # GENERAL DRAW METHOD
    def draw(self, screen, draw_features = True, is_playback = False):
        # start drawing highway lanes at x_offset
        curr_x, y = self.x_offset, 0
        # draw road (just rectangle without lane markings)
        self.draw_road(screen, curr_x, y)
    
        # draw lane markings.Timestep parity allows for the illusion of movement 
        # add "new" dashed lines at the origin after prev was translated down
        self.odd_timestep = not self.odd_timestep

        start_y = y if self.odd_timestep else y + self.down_speed

        curr_x = self.x_offset

        # draw dashed lanes
        for i in range(self.num_lanes):
            self.draw_dashed_lane(screen, curr_x, start_y)
            curr_x += self.lane_width
        
        # draw boundary lanes (overwriting the dashed lanes at the sides)
        self.draw_solid_lane(screen, curr_x, y)
        self.draw_solid_lane(screen, self.x_offset, y)

        # draw cars, record the agent car (it is special to state).
        agent_car = None

        for car in self.car_list:
            car.draw(screen, is_playback);    
            
            if (car.id == 1): 
                agent_car = car  

        if draw_features and not is_playback:
            # draw agent car features
            x, curr_y  = self.lane_width * (self.num_lanes + 1) + 100, 10
            if agent_car:
                # draw agent car features
                self.draw_agent_car(agent_car, screen, x, curr_y)
                # draw speed limit and agent car current speed
                self.draw_agent_speeds(agent_car.max_speed, \
                    agent_car.speed, screen)
                # draw simulator inputs: acceleration, angle
                curr_y += 200
                self.draw_simulator_inputs(agent_car, screen, x, curr_y)

            # draw highway state
            curr_y += 150
            self.draw_highway_state(screen, x, curr_y) 


    
