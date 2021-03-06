import pygame
from math import pi, radians
from constants import *
from helpers import *

# Simulator has 4 components: steering wheel (angle), and 
# brake, acceleration, clutch pedals (percentage of how far pressed)

class Simulator:

  # set up Simulator
  def init_simulator(self):
    self.simulator = None

    for j in range(0,pygame.joystick.get_count()):
      if pygame.joystick.Joystick(j).get_name() == SIMULATOR_NAME:
        self.simulator = pygame.joystick.Joystick(j)
        self.simulator.init() # pygame joystick init
        print("Found Driving Simulator ", self.simulator.get_name())

    if not self.simulator:
      print("Did not find Driving Simulator ", SIMULATOR_NAME)

  def __init__(self, accel_max=10, degree_max=540):
    self.accel_max  = accel_max
    self.degree_max = degree_max

    # u1 = acceleration, u2 = steering angle (radians)
    self.prev_u1 = 0
    self.prev_u2 = 0

    self.u1 = 0
    self.u2 = 0

    # set up Simulator
    self.init_simulator()

  def __str__(self):
    res = "======SIMULATOR========\n"
    res += "Name: "
    res += self.simulator.get_name() if self.simulator else "Manual"
    res += ("\nAccel & Deg Max: %1.2f %1.2f" % (self.accel_max, self.degree_max))
    res += "\nCurrent Inputs: u1 = %1.2f, u2 = %1.2f" % (self.u1, self.u2)
    res += "\n======SIMULATOR========"
    return res

  # axis val are between -1 to 1, convert to percentage between 0 and 1
  def val_to_percent(self, val): 
    return (1 - val) * 0.5

  # convert -1 to 1 to angle -540 to 540 degrees. (degree max = 540 = 360 + 180) 
  def val_to_degrees(self, val):   
    sign = 1 if val > 0 else -1
    return -1 * sign * ((abs(val) * self.degree_max) % 360)


  def val_to_u2(self, val):  
    vertical_degree = self.val_to_degrees(val)
    u2 = radians(vertical_degree) 
    return u2

  # convert accel from percentage to value between 0 and 5 (accel max)
  def val_to_accel(self, val):
    percentage = self.val_to_percent(val)
    accel = self.accel_max * percentage
    return accel


  def get_axis(self, axis):
    if axis == STEERING_WHEEL_AXIS:    
      return self.u2
    elif axis == ACCELERATOR_PEDAL_AXIS or axis == BRAKE_PEDAL_AXIS: 
      return self.u1
    else:
      print("Axis %d not configured" % axis)

  def update_u1(self, new_u1):
    self.prev_u1 = self.u1
    self.u1 = new_u1

  def update_u2(self, new_u2):
    self.prev_u2 = self.u2
    self.u2 = new_u2

  # u1 = acceleration, u2 = steering angle (radians)
  def set_axis(self, axis, val, discrete=True):  

    new_u1 = self.val_to_accel(val)
    new_u2 = self.val_to_u2(val)

    if discrete:
      new_u1 = discretize_within_range(new_u1, -1, 1, 0.2)
      new_u2 = discretize_within_range(new_u1, -radians(30), radians(30), \
                                                radians(15))


    if axis == STEERING_WHEEL_AXIS:      self.update_u2(new_u2)
    elif axis == ACCELERATOR_PEDAL_AXIS: self.update_u1(new_u1)
    elif axis == BRAKE_PEDAL_AXIS:       self.update_u1(-1 * new_u1)
    
    else:
      print("Axis %d not configured" % axis)
