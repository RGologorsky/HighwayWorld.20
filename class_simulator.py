import pygame
from constants import *

# Simulator has 4 components: steering wheel (angle), and 
# brake, acceleration, clutch pedals (percentage of how far pressed)

# useful constants
# SIMULATOR_NAME = "G920 Driving Force Racing Wheel for Xbox One"
# STEERING_WHEEL_AXIS    = 0
# ACCELERATOR_PEDAL_AXIS = 1 
# BRAKE_PEDAL_AXIS       = 2
# CLUTCH_PEDAL_AXIS      = 3

# AXIS_NAMES = ["STEERING_WHEEL_AXIS", "ACCELERATOR_PEDAL_AXIS", \
#               "BRAKE_PEDAL_AXIS", "CLUTCH_PEDAL_AXIS"]

class Simulator:

  # axis val are between -1 to 1, convert to percentage between 0 and 1
  def val_to_percent(val): 
    return (1 - val) * 0.5

  # convert -1 to 1 to angle -540 to 540 degrees. (540 = 360 + 180) 
  def val_to_angle(val):   
    return (val * 540) % 360


  def __init__(self, agent_car):

    # set up '
    self.simulator = None
    self.agent_car = agent_car
    
    # set up Simulator
    for j in range(0,pygame.joystick.get_count()):
      if pygame.joystick.Joystick(j).get_name() == SIMULATOR_NAME:
        self.simulator = pygame.joystick.Joystick(j)
        self.simulator.init() # pygame joystick init
        print("Found Driving Simulator ", self.simulator.get_name())

    if not self.simulator:
      print("Did not find Driving Simulator ", SIMULATOR_NAME)


  def get_state(self):
    return (self.agent_car.angle, self.agent_car.acceleration, \
            self.agent_car.brake)

  def get_axis(self, axis):
    if   axis == STEERING_WHEEL_AXIS:    return self.agent_car.angle
    elif axis == ACCELERATOR_PEDAL_AXIS: return self.agent_car.acceleration
    elif axis == BRAKE_PEDAL_AXIS:       return self.agent_car.brake
    else:
      print("Axis %d not configured" % axis)


  def set_axis(self, axis, val):  

    new_val = Simulator.val_to_percent(val)

    if axis == STEERING_WHEEL_AXIS:
      new_val = Simulator.val_to_angle(val) 

    if axis == STEERING_WHEEL_AXIS:    
      self.agent_car.update_angle(new_val)
    elif axis == ACCELERATOR_PEDAL_AXIS: 
      self.agent_car.update_acceleration(new_val)
    elif axis == BRAKE_PEDAL_AXIS:       
      self.agent_car.update_brake(new_val)
    else:
      print("Axis %d not configured", axis)

    print("Set ", AXIS_NAMES[axis], " to ", val)

  
