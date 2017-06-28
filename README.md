# HighwayWorld 2.0: A toy world simulating a highway with cars.

# Agent Car is controlled by human input

# Other Car refers to all other cars on the road

# Simplest policy: other cars start with a speed taken from a Normal distribution, where the mean is determined by the lane number (left lane cars tend to go faster, right lane cars slower, etc). Other cars have a "preferred lane," i.e. they try to stay in the lane they started out with. When approaching a car in front, they match the other car's speed.

# Todo: implement passing behavior.

# Notes:

Normal speeds => continuous => large state space, continuous position 
I round lane position to nearest integer.

# highway speed limit? Cut off normal distr since speed > 0.5 (so round > 0)
# other car's keep a distance of self.WIDTH/2 away from each other

# Highway

# highway state: for each highway position = (lane, lane_pos), record: car id # and speed.


# agent car creaed first => id = 0 -> used to print agent car state

# Pygame wheel turns 540 degrees (360 + 180)
# only using brake, acceleration, and steering wheel, not clutch or buttons
