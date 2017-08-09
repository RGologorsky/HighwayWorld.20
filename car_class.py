import pygame
from constants import *
from abstract_car import AbstractCar
from math import *
from dynamics_model import *
from helpers import *

from random import choice

# pygame.sprite.Sprite
class OtherCar(AbstractCar):

    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1, \
        role="other", file_name="other_car"):

        self.original_file_name = AbstractCar.data + "/" + file_name
        self.file_name = self.original_file_name
        self.file_ext = ".png"


        super().__init__(highway, simulator, lane, lane_pos, speed, role)

        self.keep_distance = self.HEIGHT/2
        self.preferred_lane = self.lane # prefer original starting lane
        self.preferred_speed = self.speed # prefer original speed
        
        self.passing_threshold = 2 # how much slowdown will tolerate
        self.am_passing = False

        self.role = role

    # returns DONE = False since other cars don't collide with one another
    def move(self):   
        super().move(allow_collision = False, check_distance = True)
        return False

class SchoolBus(OtherCar):
    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1, \
        role="school_bus", file_name="school_bus"):

        super().__init__(highway, simulator, lane, lane_pos, speed, role, file_name)

class LongTruck(OtherCar):
    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1, \
        role="long_truck", file_name="long_truck"):

        super().__init__(highway, simulator, lane, lane_pos, speed, role, file_name)

class MediumTruck(OtherCar):
    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1, \
        role="medium_truck", file_name="medium_truck"):

        super().__init__(highway, simulator, lane, lane_pos, speed, role, file_name)

class MergingCar(AbstractCar):

    def __init__(self, highway, agent_car, simulator, lane=-1, lane_pos=-1, speed=-1, role="B"):

        self.original_file_name = AbstractCar.data + "/other_car"
        self.file_name = self.original_file_name
        self.file_ext = ".png"


        super().__init__(highway, simulator, lane, lane_pos, speed, role)

        self.keep_distance = self.HEIGHT
        self.preferred_lane = self.lane # prefer original starting lane
        self.preferred_speed = self.speed # prefer original speed
        
        self.passing_threshold = 2 # how much slowdown will tolerate
        self.am_passing = False

        self.agent_car = agent_car
        self.left_blinker = True


    # returns DONE
    def move(self): 
        self.check_distance()

        # apply constant acceleration, linear increase speed
        self.simulator.u1 = 0.10


        # if ahead of car A by margin, begin turning wheel to 45 degrees
        if (self.lane_pos > self.agent_car.lane_pos + self.HEIGHT/5):
            self.simulator.u2 += radians(5)


        # project position forward in 2 time steps
        is_collision = self.highway.crash_in_n_steps(2)

        while is_collision:
            print("forecast is collision")

            # stop accelerating
            self.simulator.u1 = 0

            # start turning wheel back if was turning into other lane
            if self.heading > radians(90):
                self.simulator.u2 -= radians(5)
            else:
                self.simulator.u2 = 0

            # project position forward in 2 time steps w/ new accel and steering
            is_collision = self.highway.crash_in_n_steps(2)

        
        # no collision forecasted

        (new_x, new_y, new_speed, new_heading) = \
            next_step(self.x, self.y, self.speed, self.heading, \
                self.simulator.u1, self.simulator.u2, self.l_r, self.l_f)

        
        # update lane, lane pos
        new_lane, new_lane_pos = self.pixel_to_lane_pos(new_x, new_y)

        self.heading = new_heading

        if self.is_legal_speed(new_speed):
            self.speed = new_speed

        if self.is_legal_pos(new_x, new_y, new_heading):
            self.x, self.y           = new_x, new_y
            self.lane, self.lane_pos = new_lane, new_lane_pos

            if self.lane == 0:
                print("merge success")
                DONE = True # SUCCESSFULLY MERGED IN
                return DONE
        else:
            self.y -= self.speed
            self.lane, self.lane_pos = self.pixel_to_lane_pos(self.x, self.y)
        self.rotate()

        # if behind car A by margin, done
        if (self.lane_pos < self.agent_car.lane_pos - 2 * self.HEIGHT):
            print("merge failed")
            DONE = True
            return DONE
  
        return False

class AgentCar(AbstractCar):


    def init_start_state(self):
        self.trajectory.append(self.get_feature())

    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1, role="agent", file_name = ""):
        AbstractCar.reset_counter();

        self.trajectory = []

        if not file_name:
            # choice(["other_car", "long_truck", "medium_truck"])
            file_name = "other_car"

        self.original_file_name = AbstractCar.data + "/" + file_name
        # self.original_file_name = AbstractCar.data + "/agent_car"
        self.file_name = self.original_file_name
        self.file_ext = ".png"

        # self.WIDTH = 44 #228
        # self.HEIGHT = 100 #128

        super().__init__(highway, simulator, lane, lane_pos, speed, role)
        

    # returns whether game is DONE
    # when agent car moves, new highway track comes down (eg stays in place)
    # moves all other cars/reference point down
    
    # def get_state(self):


    def move(self):

        old_y = self.y
        collision = super().move(allow_collision = True, check_legal_pos = True);
        new_y = self.y

        amt_back = old_y - new_y # flipped orientation, y inc from top-down
        # update trajectory
        self.trajectory.append(Z)
        curr_feature = self.get_feature()
        self.trajectory.append(curr_feature)

                
        reached_end = self.lane_pos >= self.highway.highway_len - 1
        game_ended = collision or reached_end

        if game_ended:
            if collision: print("Collision Occurred")
            if reached_end: print("Successfully Reached End of Track")
         
        # let highway draw functions know to drop down
        self.set_all_cars_back(amt_back)

        return game_ended

    def change_lane(self, dir):

        super().change_lane(dir)
        
        self.trajectory.append(L if dir == -1 else R)
        self.trajectory.append(self.get_feature())
        
        
    def change_speed(self, speed_change_dir):
        super().change_speed(speed_change_dir)

        self.trajectory.append(S if dir == -1 else F)
        self.trajectory.append(self.get_feature())

    def print_trajectory(self, trajectory):

        action_to_string = {
            Z: "No Change", 
            F: "Faster", 
            S: "Slower", 
            L: "Left", 
            R: "Right"
        }

        print("Human-Readable Trajectory Playback")
        
        len_traj = len(trajectory)
        print("Len of trajectory: ", len_traj)
        for i in range(0, len_traj - 1, 2):
            print("State %d" % (i/2))
            self.print_feature(trajectory[i])

            print("Action %d: %s" % ((i/2), action_to_string[trajectory[i + 1]]))

    def print_simulator_settings(self):
        res =  "Agent Car \n"
        res += "Lane %2.2f. Lane Pos %2.2f: \n" % (self.lane, self.lane_pos)
        res += "Speed %2.2f: \n" % self.speed
        res += "Heading: %2.2d deg. \n"   % degrees(self.heading)       
        res += "Acceleration: %2.2f (0-5 scale). \n" % self.simulator.u1
        res += "Steering Angle: %2.2f deg. \n" % degrees(self.simulator.u2)
        return res
