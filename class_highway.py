import pygame
from constants import *
import numpy as np
from irlworld import *

"""
Implements the Highway World 2.0 environment

"""

class Highway(IRLworld):


    # state vector:  index corresponds to lane and lane_positino 
    # value = (car id, car_speed) at lane and lane_position given by index
    
    lane_sep_color = WHITE
    lane_color = GRAY
    
    lane_height = 75 # lane_height = 150 # little more than Car.height
    lane_unit_length = 1

    car_list = []
    
    def __init__(self,num_lanes=3, highway_len = 1100, num_speeds = 4, max_num_cars=10, discount = 0.8):

        self.num_lanes = num_lanes
        self.highway_len = highway_len
        self.lane_width = highway_len * self.lane_unit_length

        self.num_states = num_lanes*highway_len
        self.state = [(-1, -1)] * self.num_states

        ############################
        # HIGHWAY WORLD ATTRIBUTES
        #############################
        # actions = left, right, slower, faster, zero change
        # state = lane, lane_pos, speed

        self.actions = (Z, L, R, S, F)
        self.n_actions = len(self.actions)
        self.n_states = \
            num_lanes * highway_len * (num_speeds + 1) * (max_num_cars + 1)
        self.discount = discount

        # Construct the transition probability array
        self.transition_probability = np.array(
            [[[self._transition_probability(i,j,k)
               for k in range(self.n_states)]
              for j in range(self.n_actions)]
             for i in range(self.n_states)])

    def get_state_index(self, curr_lane, curr_lane_pos):
        return curr_lane * self.highway_len + curr_lane_pos

    def deciper_index(self, index):
        return (index/self.highway_len, index % self.highway_len)

    def get_state_elem(self, lane, lane_pos):
        idx = self.get_state_index(lane, lane_pos)
        if idx < 0 or idx >= self.num_states:
            print("state elem, looking @ index %d" % idx)
            print("lane %d, lane_pos %d" % (lane, lane_pos))
        return self.state[idx]

    def __str__(self):
        res = "Highway State. \n"
        for i in range(self.num_states):
            elem = self.state[i]
            if elem != -1:
                lane, lane_pos = self.deciper_index(i)
                res += ("Lane = %d, Pos = %d. Speed = %d, ID = %d. \n" % \
                    (lane, lane_pos, elem[0], elem[1]))
        return res

    def print_state(self):
        return print(str(self))

    def get_closest_cars(self, curr_lane, curr_lane_pos):
        closest_cars = []
        for lane in range(self.num_lanes):
            
            num_steps_ahead = 0 if lane != curr_lane else 1
            num_steps_behind = 0 if lane != curr_lane else 1

            ahead_state_elem = \
                self.get_state_elem(lane, curr_lane_pos + num_steps_ahead)
            behind_state_elem = \
                self.get_state_elem(lane, curr_lane_pos - num_steps_behind)
            
            while (curr_lane_pos + num_steps_ahead < self.highway_len - 1 and \
                    ahead_state_elem == -1):

                num_steps_ahead += 1
                ahead_state_elem = \
                    self.get_state_elem(lane,curr_lane_pos+num_steps_ahead)
            
            while (curr_lane_pos - num_steps_behind > 0 and \
                behind_state_elem == -1):
    
                num_steps_behind += 1
                behind_state_elem = \
                    self.get_state_elem(lane,curr_lane_pos-num_steps_behind)

            # no car ahead
            if ahead_state_elem == -1:
                num_steps_ahead = -1
                ahead_car_speed = -1
            
            else: 
                ahead_car_speed = ahead_state_elem[1]

            # no car behind
            if behind_state_elem == -1:
                num_steps_behind = -1
                behind_car_speed = -1
            
            else: 
                behind_car_speed = behind_state_elem[1]
            

            closest_cars.append(num_steps_ahead)
            closest_cars.append(ahead_car_speed)

            closest_cars.append(num_steps_behind)
            closest_cars.append(behind_car_speed)

            my_speed = get_state_elem

        return closest_cars

    def is_car_in_range(curr_lane, curr_lane_pos, start, steps_away_max, ahead):
        away_dir = 1 if ahead else -1

        num_steps_away = start * away_dir

        (car_id, car_speed) = \
                self.get_state_elem(lane, curr_lane_pos + num_steps_away)
        
            while (curr_lane_pos + num_steps_away < steps_away_max and \
                    ahead_state_elem == (-1, -1)):

                num_steps_away += away_dir

                (car_id, car_speed) = \
                self.get_state_elem(lane, curr_lane_pos + num_steps_away)
            




    def get_closest_cars_bool(self, curr_lane, curr_lane_pos):
        # return boolean vector of whether the closest cars in each lane
        # are 1-50 steps away, 50-150 steps away, or 250+ steps away
        maxes = [50, 150, 250, self.highway_len - 1]
        num_maxes = len(maxes)
        closest_cars = []
        for lane in range(self.num_lanes):
            for i in range(num_maxes):
                steps_away_max = maxes[i]
                start = maxes[i - 1] if i != 0 else (lane != curr_lane)
                
                (num_steps_ahead, ahead_car_speed) =
                    self.is_car_in_range(curr_lane, curr_lane_pos, \
                                            start, steps_away_max, ahead=True)
                
                (num_steps_behind, behind_car_speed) =
                    self.is_car_in_range(curr_lane, curr_lane_pos, \
                        start, steps_away_max, ahead=False)


                closest_cars.append(num_steps_ahead)
                closest_cars.append(ahead_car_speed)

                closest_cars.append(num_steps_behind)
                closest_cars.append(behind_car_speed)

        return closest_cars
    def feature_vector(self, state_index):
        """
        Return feature vector of the state specified by the index i

        i : State index
        """

        lane, lane_pos = self.deciper_index(state_index)
        curr_elem = self.state[state_index]
        my_speed = -1 if curr_elem == -1 else curr_elem[1]

        closest_cars = self.get_closest_cars(lane, lane_pos)
        closest_cars.append(my_speed)

        return closest_cars

    def feature_matrix(self):
        """
        Return the feature matrix for the entire Highway world

        """
        features = []
        for n in range(self.n_states):
            f = self.feature_vector(n)
            features.append(f)
        return np.array(features)

    def index_to_state(self, state_index):
        """
         Returns the state for the given index

        i : State index
        """
        return self.deciper_index(state_index)

    def state_to_index(self, state):
        """
        Returns the index for the given state

        state: (lane, lane_pos, speed, id_num)
        """
        (lane, lane_pos, speed, id_num) = state

        # for consisent indexing
        if speed == -1:
            speed = 0

        return lane * self.highway_len + 
        (index/self.highway_len, index % self.highway_len)

    def neighboring(self, i, k):
        """
        Returns if the two states i and k (given by coordinates) are neighbors. Also,
        returns true if they are the same point.

        i : (x,y) int tuple
        k : (x,y) int tuple
        """
       return abs(i[0] - k[0]) <= 1 and abs(i[1] - k[1]) <= 1

    def _transition_probability(self, i, j, k):
        """
        Returns the probability of transitioning from state i to state k given
        action j

        i : State int
        j : Action int
        k : State int
        """
        
        lane_i, lane_pos_i = self.index_to_state(i)
        action_j = self.actions[j]
        lane_k, lane_pos_k = self.index_to_state(k)

        if not self.neighboring((xi, yi), (xk, yk)):
            return 0

        if (xi + xj, yi + yj) == (xk, yk):
            return 1 - self.wind + self.wind/self.n_actions

        if (xi, yi) != (xk, yk):
            return self.wind/self.n_actions

        # Both are the same point, we can only move here by either moving
        # off the grid or being blown off the grid. Are we on a corner or not?
        if (xi, yi) in {(0,0), (self.grid_size - 1, self.grid_size - 1)
                        (0, self.grid_size - 1), (self.grid_size - 1, 0)}:
            # Corner
            # Was the action intended to move it off the grid
            if not (0 <= xi + xj < self.grid_size and 0 <= yi+yj < self.grid_size):
                # Yes
                # 2 because we can go off-grid in two ways 
                return 1 - self.wind + 2*self.wind/self.n_actions
            else:
                # No
                return 2*self.wind/self.n_actions
        else:
            # Not a Corner
            # An edge?
            if (xi not in {0, self.grid_size-1} and
                yi not in {0, self.grid_size-1}):
                # No
                return 0
            else:
                # Yes
                # Was the action intended to move it off the grid
                if not (0 <= xi+xj < self.grid_size and 0<= yi+yj < self.grid_size):
                    # Yes
                    return 1 - self.wind + self.wind/self.n_actions
                else:
                    # No
                    return self.wind/self.n_actions
        return 0

    def add_car(self, car_id, car_lane, car_lane_pos, curr_speed):
        state_index = self.get_state_index(car_lane, car_lane_pos)
        self.state[state_index] = (car_id, curr_speed)

    def remove_car(self, car_lane, car_lane_pos):
        state_index = self.get_state_index(car_lane, car_lane_pos)
        self.state[state_index] = -1

    def update_car(self, car_id, old_lane, old_lane_pos, new_lane, new_lane_pos, curr_speed):
        self.remove_car(old_lane, old_lane_pos)
        self.add_car(car_id, new_lane, new_lane_pos, curr_speed)

        # self.print_state()

    def draw_lane(self, screen, x, y):
        pygame.draw.rect(screen, self.lane_color, [x,y,self.lane_width,self.lane_height], 0)

    def draw_sep(self, screen, x, y):
        pygame.draw.line(screen, self.lane_sep_color, (x,y), (x + self.lane_width, y), 1)


    def draw(self, screen):
        # start at top-left
        x = 0
        curr_y = 0
        
        # draw lanes
        for i in range(self.num_lanes):
            
            self.draw_lane(screen, x, curr_y)
            curr_y += self.lane_height
            
            self.draw_sep(screen, x, curr_y)
            curr_y += 1

        # draw cars
        for car in self.car_list:
            car.draw(screen);
