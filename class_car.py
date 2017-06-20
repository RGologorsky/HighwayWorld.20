import pygame
from constants import L,R,S,F,Z # actions
from abstract_car import AbstractCar

class OtherCar(AbstractCar):
    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        super().__init__(highway, lane, lane_pos, speed)
        self.image_car = pygame.image.load(AbstractCar.data + "/other_car.png").convert()
    # returns whether game is DONE
    # other cars don't collide with one another with some probability
    def move(self):
        new_lane, new_lane_pos = self.lane, self.lane_pos + self.speed

        if self.is_collision(new_lane, new_lane_pos):
            print("Move would cause collision between other cars")
            return False
        
        super().move()
        return False

class AgentCar(AbstractCar):
    def __init__(self, highway, lane=-1, lane_pos=-1, speed=-1):
        super().__init__(highway, lane, lane_pos, speed)
        self.image_car = pygame.image.load(AbstractCar.data + "/agent_car.png").convert()
        self.trajectory = []
    
    def set_start_state(self):
        self.trajectory.append(self.get_feature())
    # returns whether game is DONE
    def move(self):
        new_lane, new_lane_pos = self.lane, self.lane_pos + self.speed
        collision = self.is_collision(new_lane, new_lane_pos)
        super().move();
        # self.highway.print_state()
        self.trajectory.append(Z)
        self.trajectory.append(self.get_feature())
        self.print()
        if collision:
            print("Trajectory: ", self.trajectory)
        
        reached_end = self.lane_pos >= self.highway.highway_len
        game_ended = collision or reached_end

        print("Features: ", self.get_feature())

        return game_ended

    def change_lane(self, dir):

        new_lane, new_lane_pos = self.lane + dir, self.lane_pos + self.speed 

        if not self.is_legal_pos(new_lane, new_lane_pos):
            return

        collision = self.is_collision(new_lane, new_lane_pos)
        super().change_lane(dir)
        
        self.trajectory.append(L if dir == -1 else R)
        self.trajectory.append(self.get_feature())
        if collision:
            print("Trajectory: ", self.trajectory)
        return collision
        # self.highway.
        # self.trajectory.append()
        
    def change_speed(self, speed_change):
        super().change_speed(speed_change)
        self.trajectory.append(S if dir == -1 else F)
