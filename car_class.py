import pygame
from constants import *
from abstract_car import AbstractCar
from math import *

# pygame.sprite.Sprite
class OtherCar(AbstractCar):

    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1):

        self.original_file_name = AbstractCar.data + "/other_car"
        self.file_name = self.original_file_name
        self.file_ext = ".png"

        super().__init__(highway, simulator, lane, lane_pos, speed)

        self.keep_distance = self.HEIGHT/2
        self.preferred_lane = self.lane # prefer original starting lane
        self.preferred_speed = self.speed # prefer original speed
        
        self.passing_threshold = 2 # how much slowdown will tolerate
        self.am_passing = False

    # returns DONE = False since other cars don't collide with one another
    def move(self):   
        super().move(allow_collision = False, check_distance = True)
        return False

class MergingCar(AbstractCar):

    def __init__(self, highway, agent_car, simulator, lane=-1, lane_pos=-1, speed=-1):

        self.original_file_name = AbstractCar.data + "/other_car"
        self.file_name = self.original_file_name
        self.file_ext = ".png"

        super().__init__(highway, simulator, lane, lane_pos, speed)

        self.keep_distance = self.HEIGHT/2
        self.preferred_lane = self.lane # prefer original starting lane
        self.preferred_speed = self.speed # prefer original speed
        
        self.passing_threshold = 2 # how much slowdown will tolerate
        self.am_passing = False

    # returns DONE = False since other cars don't collide with one another
    def move(self):   
        super().move(allow_collision = False, check_distance = True)
        return False

class AgentCar(AbstractCar):


    def init_start_state(self):
        self.trajectory.append(self.get_feature())

    def __init__(self, highway, simulator, lane=-1, lane_pos=-1, speed=-1):
        AbstractCar.reset_counter();

        self.trajectory = []

        self.original_file_name = AbstractCar.data + "/agent_car"
        self.file_name = self.original_file_name
        self.file_ext = ".png"

        super().__init__(highway, simulator, lane, lane_pos, speed)
        

    # returns whether game is DONE
    # when agent car moves, new highway track comes down (eg stays in place)
    # moves all other cars/reference point down
    def move(self):

        collision = super().move(allow_collision = True);
        
        # update trajectory
        self.trajectory.append(Z)
        curr_feature = self.get_feature()
        self.trajectory.append(curr_feature)

                
        reached_end = self.lane_pos >= self.highway.highway_len - 1
        game_ended = collision or reached_end

        if game_ended:
            if collision: print("Collision Occurred")
            if reached_end: print("Successfully Reached End of Track")
         
        self.highway.increment = self.highway.max_increment * self.speed/self.max_speed            
        self.set_all_cars_back()

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
