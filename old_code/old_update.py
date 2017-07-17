    # update functions

    # update pos returns whether updated position caused collision
    def update_pos(self, allow_collision = False):
        angle = radians(self.angle)

        
        new_x = self.x + self.speed * sin(angle)
        new_y = self.y - self.speed * cos(angle)

        new_lane, new_lane_pos = self.pixel_to_lane_pos(new_x, new_y)

        if self.is_legal_lane(new_lane): 
            yes_collision = self.is_collision(new_x, new_y, self.angle)
            
            if allow_collision or not yes_collision:
                self.x, self.y           = new_x, new_y
                self.lane, self.lane_pos = new_lane, new_lane_pos

                return yes_collision
        return False

    def update_speed(self):
        friction = 0.2

        new_speed = self.speed

        if self.acceleration != 0:
            new_speed += 2* self.acceleration - friction*self.speed

        if self.brake != 0:
            new_speed -= 3* self.brake - friction*self.speed

        if self.is_legal_speed(new_speed): 
            self.speed = new_speed
