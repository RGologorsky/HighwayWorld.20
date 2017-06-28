# closest cars in each lane
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

            # my_speed = self.get_state_elem

        return closest_cars

############################
        # HIGHWAY WORLD ATTRIBUTES
        #############################
        # actions = left, right, slower, faster, zero change
        # state = lane, lane_pos, speed

        # self.num_speeds = num_speeds
        # self.actions = (Z, L, R, S, F)
        # self.n_actions = len(self.actions)
        # self.n_states = \
        #     num_lanes * highway_len * num_speeds # * (max_num_cars + 1)
        # self.discount = discount

        # Construct the transition probability array
        # self.transition_probability = np.array(
        #     [[[self._transition_probability(i,j,k)
        #        for k in range(self.n_states)]
        #       for j in range(self.n_actions)]
        #      for i in range(self.n_states)])

# def is_car_in_range(curr_lane, curr_lane_pos, start, steps_away_max, ahead):
    #     away_dir = 1 if ahead else -1

    #     num_steps_away = start * away_dir

    #     (car_id, car_speed) = \
    #             self.get_state_elem(lane, curr_lane_pos + num_steps_away)
        
    #         while (curr_lane_pos + num_steps_away < steps_away_max and \
    #                 ahead_state_elem == (-1, -1):

    #             num_steps_away += away_dir

    #             (car_id, car_speed) = \
    #             self.get_state_elem(lane, curr_lane_pos + num_steps_away)
            




    # def get_closest_cars_bool(self, curr_lane, curr_lane_pos):
    #     # return boolean vector of whether the closest cars in each lane
    #     # are 1-50 steps away, 50-150 steps away, or 250+ steps away
    #     maxes = [50, 150, 250, self.highway_len - 1]
    #     num_maxes = len(maxes)
    #     closest_cars = []
    #     for lane in range(self.num_lanes):
    #         for i in range(num_maxes):
    #             steps_away_max = maxes[i]
    #             start = maxes[i - 1] if i != 0 else (lane != curr_lane)
                
    #             (num_steps_ahead, ahead_car_speed) =
    #                 self.is_car_in_range(curr_lane, curr_lane_pos, \
    #                                         start, steps_away_max, ahead=True)
                
    #             (num_steps_behind, behind_car_speed) =
    #                 self.is_car_in_range(curr_lane, curr_lane_pos, \
    #                     start, steps_away_max, ahead=False)


    #             closest_cars.append(num_steps_ahead)
    #             closest_cars.append(ahead_car_speed)

    #             closest_cars.append(num_steps_behind)
    #             closest_cars.append(behind_car_speed)

    #     return closest_cars
