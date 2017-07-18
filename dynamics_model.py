# dynamics model = kinematic bicycle model
from math   import atan, tan, cos, sin, pi, radians, degrees

def slip_angle(u2, l_r, l_f):
        return atan(tan(u2) * l_r/(l_f + l_r))

# kinematic bicycle model, center of mass at center of car
def next_step(x, y, v, psi, u1, u2, l_r, l_f):

    # print("input")
    # print("x, y, v, psi, u1, u2")
    # print(x, y, v, psi, u1, u2)
    # print("l_r, l_f", l_r, l_f)

    alpha = 0.2

    beta = slip_angle(u2/5.0, l_r, l_f)
    delta_x = v * cos(psi + beta)
    delta_y = v * sin(psi + beta)
    delta_v = u1
    # delta_v = u1 - alpha * v
    delta_psi = v/l_r * sin(beta)

    # print("delta_x", delta_x)
    # print("delta_y", delta_y)
    # print("delta_psi (deg)", degrees(delta_psi))
    alpha = 0.2
    new_x   = x + delta_x
    new_y   = y + delta_y
    new_v   = v + delta_v
    new_psi = (psi + delta_psi) % (2*pi)

    # psi (radians) betwwen 0 and 2pi
    # psi_sign = 1 if new_psi > 0 else -1
    # new_psi =  psi_sign * (abs(new_psi) % (2*pi))

    return (new_x, new_y, new_v, new_psi)

def next_step_simple(x, y, v, psi, u1, u2, l_r, l_f):
    alpha = 0.2

    delta_x = v * cos(psi)
    delta_y = v * sin(psi)
    delta_v = u1 - alpha * v
    delta_psi = v * u2

    # print("delta_x", delta_x)
    # print("delta_y", delta_y)
    # print("angle (deg)", degrees(angle))

    new_x = x + delta_x
    new_y = y + delta_y
    new_v = v + delta_v
    new_psi = psi + delta_psi

    return (new_x, new_y, new_v, new_psi)
