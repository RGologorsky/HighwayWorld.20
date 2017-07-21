import pygame

from constants import *
from game_events     import check_event
from playback import *
from scenarios import *


# returns when DONE
def play_game(scenario_num=0):
    (highway,agent_car,simulator,draw_list,screen) = init_scenario(scenario_num)

    screen.fill(GREEN)
    DONE, PAUSE, RESTART = False, False, False

    while not (DONE or RESTART):
        for event in pygame.event.get():
            DONE,PAUSE,RESTART = check_event(event,highway,agent_car,simulator,\
                            DONE, PAUSE, RESTART);
        redraw_all(screen, draw_list)
    print("Simulation Over")

    if RESTART:
        play_game();            # restart the game

    return DONE

def playback(time):
    highway_time_series = Playback.get_recorded_data(time)

    num_time_steps = len(highway_time_series)
    curr_time_step = 0
    
    while curr_time_step != num_time_steps:
        for event in pygame.event.get():
            curr_time_step = check_playback_event(event, screen, \
                highway_time_series, curr_time_step);
    print("Playback Over")


def main():
    scenario_num = 0
    play_game(scenario_num)

    # time = "2017-07-21 08-48-24"
    # playback(time)

main()
