def pixel_to_lane_pos(self, x, y):
        lane     = int(y / self.highway.lane_height)
        lane_pos = int(round(x))

        return (lane, lane_pos)
        
def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, [x,y,self.highway_len,self.lane_height], 0)

def draw_sep(self, screen, x, y):
    step_size = int(self.highway_len/20)
    sep_size = int(step_size/2)
    for i in range(0, self.highway_len, step_size):
        curr_x = x + i
        pygame.draw.line(screen, self.lane_sep_color, \
            (curr_x,y), (curr_x + sep_size, y), 2)

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
