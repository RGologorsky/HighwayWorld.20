import pygame
from constants import *
from abstract_car import AbstractCar

# pygame.sprite.Sprite
class OtherCar(AbstractCar):

    # don't go closer than keep_dist between end of my car and start of other

    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        super().__init__(highway, lane, lane_pos, speed)
        # pygame.sprite.Sprite.__init__(self,
        #                       self.groups) 

        self.image_car = pygame.image.load(AbstractCar.data + "/other_car.png").convert()
        self.original_image = self.image_car

        self.keep_distance = self.WIDTH/2
        self.preferred_lane = self.lane # prefer original starting lane
        self.preferred_speed = self.speed # prefer original speed
        self.passing_threshold = 2 # how much slowdown will tolerate
        self.am_passing = False

    # def pass_ahead_car(self, lane, lane_pos):
        # if (scar_ahead_speed )
    # checks if we are keeping our distance; adjusts speed if needed
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
            self.speed = min(self.speed, car_ahead_speed) # don't speed up

    # returns DONE = False since other cars don't collide with one another
    def move(self):
        # if necessary, set speed to ahead car speed to maintain distance 
        self.check_distance(self.lane, self.lane_pos)        
        super().move(allow_collision = False)
        return False

class AgentCar(AbstractCar):

    # speed change step size
    speed_step_size = 0.1

    def init_start_state(self):
        self.trajectory.append(self.get_feature())

    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        AbstractCar.reset_counter();

        super().__init__(highway, lane, lane_pos, speed)
        file = AbstractCar.data + "/agent_car.png"
        self.image_car = pygame.image.load(file).convert_alpha()
        self.original_image = self.image_car
        self.trajectory = []
        

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

    def update_angle(self, angle):      self.angle = angle
    def update_acceleration(self, val): self.acceleration = val
    def update_brake(self, val):        self.brake = val

    def print_simulator_settings(self):
        res =  "Agent Car: Speed %2.2f: \n" % self.speed
        res += "Angle: %2.3d degrees. \n"   % self.angle        
        res += "Acceleration: %2.3f (0-1 scale). \n" % self.acceleration
        res += "Brake: %2.3f (0-1 scale). \n" % self.brake

        return res
