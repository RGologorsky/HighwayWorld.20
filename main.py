import pygame

from constants import *
from game_events     import check_event
from playback import *
from scenarios import *
from helpers import is_quit


# returns when DONE
def play_game(scenario_num=0):
    (highway,agent_car,simulator,draw_list,screen) = init_scenario(scenario_num)

    screen.fill(GREEN)
    DONE, PAUSE, RESTART = False, False, False

    while not (DONE or RESTART):
        for event in pygame.event.get():
            DONE,PAUSE,RESTART = check_event(event,highway,agent_car,simulator,\
                            DONE, PAUSE, RESTART);
        if not PAUSE:
            redraw_all(screen, draw_list)
    print("Simulation Over")

    # keep screen alive
    # DONE = False
    # while not DONE:
    #     for event in pygame.event.get():
    #         # If user clicked close or quits
    #         if is_quit(event): 
    #             DONE = True
    #     redraw_all(screen, draw_list)

    if RESTART:
        play_game();            # restart the game

    return DONE

def play_back(time):
    screen = init_screen()
    
    (highway_param, highway_time_series) = Playback.get_recorded_data(time)

    num_time_steps = len(highway_time_series)
    curr_time_step = 0
    
    print("highway param", highway_param)
    print("car 1", highway_time_series[0][0].keys())
    while curr_time_step != num_time_steps:
        for event in pygame.event.get():
            if (event.type == PLAYBACK_HIGHWAY_EVENT):
                highway_car_list = highway_time_series[curr_time_step]
                Playback.draw_highway_snapshot(screen, highway_param, \
                                                highway_car_list)
                curr_time_step += 1
    print("Playback Over")


def main():
    scenario_num = 1
    playgame = True
    playback = not playgame

    if playgame:
        play_game(scenario_num)

    if playback:
        time = "2017-07-31 08-54-48"
        play_back(time)

main()
