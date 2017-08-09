def is_collision(self, new_x, new_y, new_angle):
        (new_top_left, new_top_right, new_back_left, new_back_right) = \
            self.get_corners(new_x, new_y, new_angle)

        # see if corners collide with any other car on the road
        for car in self.highway.car_list:
            if car == self:
                continue
            # Rect(left, top, width, height)
            (left, top) = center_to_upper_left(self, car.x, car.y)
            car_rect = pygame.Rect(left, top, self.WIDTH, self.HEIGHT)
            
            collision = car_rect.collidepoint(new_top_left) or \
                        car_rect.collidepoint(new_top_right) or \
                        car_rect.collidepoint(new_back_left) or \
                        car_rect.collidepoint(new_back_right)

            if collision:
                lane, lane_pos = self.pixel_to_lane_pos(new_x, new_y)
                print("car has collision: ", self.id, lane, lane_pos)
                print(car_rect.collidepoint(new_top_left))
                print(car_rect.collidepoint(new_top_right))
                print(car_rect.collidepoint(new_back_left))
                print(car_rect.collidepoint(new_back_right))
                return True
        return False
