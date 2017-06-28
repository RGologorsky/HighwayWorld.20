import pygame
from constants import L,R,S,F,Z # actions
from abstract_car import AbstractCar
import numpy as np
from random import randint

class OtherCar(AbstractCar):

    # don't go closer than keep_dist between end of my car and start of other

    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        super().__init__(highway, lane, lane_pos, speed)
        self.image_car = pygame.image.load(AbstractCar.data + "/other_car.png").convert()
        self.keep_distance = self.WIDTH/2

    def check_distance(self, lane, lane_pos):
        my_idx = self.highway.pos_to_idx(lane, lane_pos)

        # scan front for close cars ahead
        ahead_idx = self.highway.pos_to_idx(lane,  
                    min(self.highway.highway_len-1, \
                        lane_pos + self.WIDTH + self.keep_distance))

        no_car_ahead = True
        curr_idx = my_idx
        
        while (no_car_ahead and curr_idx <= ahead_idx):
            neighbor = self.highway.idx_to_state(curr_idx)
            no_car_ahead = (neighbor == (-1, -1)) or (neighbor[0] == self.id)
            curr_idx += 1

        if not no_car_ahead:
            car_ahead_speed = self.highway.idx_to_state(curr_idx - 1)[1]
            self.speed = car_ahead_speed
            print("Changed speed to ahead car speed = %2.2f" % car_ahead_speed)


    # returns whether game is DONE
    # other cars don't collide with one another
    def move(self):
        # if necessary, set speed to ahead car speed to maintain distance 
        self.check_distance(self.lane, self.lane_pos)
        new_lane, new_lane_pos = self.lane, int(round(self.lane_pos + self.speed))
        
        super().move()
        return False

class AgentCar(AbstractCar):

    # speed change step size
    speed_step_size = 0.1

    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        super().__init__(highway, lane, lane_pos, speed)
        self.image_car = pygame.image.load(AbstractCar.data + "/agent_car.png").convert()
        self.trajectory = []
    
    def set_start_state(self):
        self.trajectory.append(self.get_feature())

    # returns whether game is DONE
    def move(self):
        new_lane, new_lane_pos = self.lane, int(round(self.lane_pos + self.speed))
        collision = self.is_collision(new_lane, new_lane_pos)
        
        super().move();
        
        # update trajectory
        self.trajectory.append(Z)
        curr_feature = self.get_feature()
        self.trajectory.append(curr_feature)
        

        self.print_feature(curr_feature)
        
        reached_end = new_lane_pos >= self.highway.highway_len
        game_ended = collision or reached_end

        print("Game over? %s " % game_ended)

        if game_ended:
            if collision: print("Collision Occurred")
            if reached_end: print("Successfully Reached End of Track")
            
            self.print_trajectory(self.trajectory)

        return game_ended

    def change_lane(self, dir):

        super().change_lane(dir)
        
        self.trajectory.append(L if dir == -1 else R)
        self.trajectory.append(self.get_feature())
        
        
    def change_speed(self, speed_change_dir):
        super().change_speed(speed_change_dir * self.speed_step_size)

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
