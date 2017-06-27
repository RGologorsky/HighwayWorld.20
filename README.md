# HighwayWorld 2.0: A toy world simulating a highway with cars.

# Agent Car is controlled by human input

# Other Car refers to all other cars on the road

# Simplest policy: other cars start with a speed taken from a Normal distribution, where the mean is determined by the lane number (left lane cars tend to go faster, right lane cars slower, etc). Other cars have a "preferred lane," i.e. they try to stay in the lane they started out with. When approaching a car in front, they match the other car's speed.

# Todo: implement passing behavior.

# Notes:

# normal speeds => continuous => large state space
