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
        self.state = [-1] * self.num_states

        ############################
        # HIGHWAY WORLD ATTRIBUTES
        #############################
        # actions = left, right, slower, faster, zero change
        # state = lane, lane_pos, speed

        self.num_speeds = num_speeds
        self.actions = (Z, L, R, S, F)
        self.n_actions = len(self.actions)
        self.n_states = \
            num_lanes * highway_len * num_speeds # * (max_num_cars + 1)
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


    #### IRL WORLD FUNCTIONS ####

    def feature_vector(self, state_index):
        """
        Return feature vector of the state specified by the index i

        i : State index
        """

        lane, lane_pos = self.deciper_index(state_index)

        # state should correspond to a car tuple, should not be -1!
        (my_id, my_speed) = self.state[state_index]

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
        state: (lane, lane_pos, speed)
        """

        pos_index,speed =state_index/self.num_speeds,state_index%self.num_speeds
        lane, lane_pos = self.deciper_index(pos_index)

        # convert 0-indexed speed to true 1-indexed speed
        speed += 1
        
        return (lane, lane_pos, speed)

    def state_to_index(self, state):
        """
        Returns the index for the given state

        state: (lane, lane_pos, speed)
        """

        (lane, lane_pos, speed) = state

        # for consisent indexing, change speed frmo 1-indexed to 0-indexed
        speed -= 1

        pos_index = self.get_state_index(lane, lane_pos)
        pos_speed_index = pos_index * self.num_speeds + speed

        return pos_speed_index

    def _transition_probability(self, i, j, k):
        """
        Returns the probability of transitioning from state i to state k given
        action j

        # actions = left, right, slower, faster, zero change

        i : State int
        j : Action int
        k : State int
        """
        
        lane_i, lane_pos_i, speed_i = self.index_to_state(i)
        action = self.actions[j]
        lane_k, lane_pos_k, speed_k = self.index_to_state(k)

        if action == Z:
            return lane_k == lane_i and \
                   lane_pos_k == lane_pos_i + speed_i and \
                   speed_k == speed_i 

        if action == L:
            return lane_k == max(0, lane_i - 1) and \
                   lane_pos_k == lane_pos_i and \
                   speed_k == speed_i 

        if action == R:
            return lane_k == min(self.num_lanes - 1, lane_i + 1) and \
                   lane_pos_k == lane_pos_i and \
                   speed_k == speed_i 

        if action == S:
            return lane_k == lane_i and \
                   lane_pos_k == lane_pos_i and \
                   speed_k == max(1, speed_i - 1) 

        if action == F:
            return lane_k == lane_i and \
                   lane_pos_k == lane_pos_i and \
                   speed_k == min(self.num_speeds - 1, speed_i + 1) 


    def reward(self, i):
        """
        Reward for being in state specified by the given index

        i : State index. int

        Look into negative reward for collision
        """

        (lane, lane_pos, speed) = self.index_to_state(i)
        if lane_pos >= self.highway_len - 1:
            return 1
        else:
            return 0

    def average_reward(self, n_traj, traj_length, policy):
        """
        Returns the average reward obtained by following a given policy over
        n_traj trajectories of length traj_length

        policy : Map from state indices to action indices
        n_traj : Number of trajectories. int
        traj_length : Length of an episode. int
        """

        trajectories = self.generate_trajectories(n_traj, traj_length, policy)
        rewards = [[r for _, _, r in trajectory] for trajectory in trajectories]
        rewards = np.array(rewards)

        total_reward = rewards.sum(axis=1)

        return total_reward.mean(), total_reward.std()

    def optimal_policy(self, i):
        pass

    def optimal_policy_deterministic(self, i):
        pass
            
    def generate_trajectories(self, n_traj, traj_length, policy, random_start=False):
        """
        Generates n_traj trajectories with length traj_length according to 
        the given policy

        n_traj : Number of trajectories. int
        traj_length : Length of an episode. int
        policy : Map from state indices to action indices
        random_start : Whether to start randomly (default False). bool
        """

        trajectories = []
        for _ in range(n_traj):
            if random_start:
                sx, sy = rn.randint(self.grid_size), rn.randint(self.grid_size)
            else:
                sx, sy = 0, 0

            trajectory = []
            for _ in range(traj_length):
                if rn.random() < self.wind:
                    action = self.actions[rn.randint(0, self.n_actions)]
                else:
                    action = self.actions[policy(self, state_to_index((sx,sy)))]

                if ( 0<= sx + action[0] < self.grid_size and
                     0 <= sy + action[1] < self.grid_size):
                    next_sx = sx + action[0]
                    next_sy = sy + action[1]
                else:
                    next_sx = sx
                    next_sy = sy

                state_int = self.state_to_index((sx,sy))
                action_int = self.actions.index(action)
                next_state_int = self.state_to_index((next_sx, next_sy))
                reward = self.reward(next_state_int)
                trajectory.append((state_int, action_int, reward))

                sx = next_sx
                sy = next_sy
                
            trajectories.append(trajectory)

        return np.array(trajectories)            
