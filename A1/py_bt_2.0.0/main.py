#
# Behavior Tree framework for A1 Behavior trees assignment.
# CS 131 - Artificial Intelligence
#
# version 2.0.0 - copyright (c) 2023 Santini Fabrizio. All rights reserved.
# Edited by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: Main function for implementing the behavior tree

import bt_library as btl
import random

from bt.behavior_tree import tree_root
from bt.behavior_tree import clean_selec
from bt.behavior_tree import gen_seq
from bt.behavior_tree import dusty_priority
from bt.behavior_tree import dusty_seq1
from bt.behavior_tree import dusty_seq2
from bt.behavior_tree import spot_seq
from bt.behavior_tree import battery_seq
from bt.behavior_tree import vac_done
from bt.globals import BATTERY_LEVEL, GENERAL_CLEANING, SPOT_CLEANING, DUSTY_SPOT_SENSOR, HOME_PATH, CLEAN_FLOOR, TIMER

# Main body of the assignment
current_blackboard = btl.Blackboard()
current_blackboard.set_in_environment(BATTERY_LEVEL, 31)
current_blackboard.set_in_environment(SPOT_CLEANING, False)
current_blackboard.set_in_environment(GENERAL_CLEANING, False)
current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)
current_blackboard.set_in_environment(HOME_PATH, "")
current_blackboard.set_in_environment(CLEAN_FLOOR, False)
current_blackboard.set_in_environment(TIMER, 30)

done = False  # bool for loop termination
spot_cycle = 0  # tracks the spot cleaning task cycle
dusty_spot = False  # bool for dusty sensor simulation
sensor_cycle = 0  # keeps track of the sensor simulation and prevents its interference to ongoing dusty_sensor task
command_cycle = False  # prevents interference of the ongoing task by regulating the frequency of user command inquiry
task_done = False  # tracks task completion for termination of the loop
spot_clean = False  # bool for spot cleaning
gen_clean = False  # bool for general cleaning

while not done:

    # get current battery level, and change the battery level
    curr_battery = current_blackboard.get_in_environment(BATTERY_LEVEL, 0)
    battery_dec = random.random() % 5
    curr_battery = curr_battery - battery_dec if curr_battery > battery_dec else 0
    current_blackboard.set_in_environment(BATTERY_LEVEL, curr_battery)

    # dusty spot sensor simulation
    # sensor simulated on every first cycle of the loop or the sensor
    if sensor_cycle == 0:
        dusty_spot = random.choice([True, False])
        if dusty_spot:
            sensor_cycle = sensor_cycle + 1
            current_blackboard.set_in_environment(DUSTY_SPOT_SENSOR, dusty_spot)

    # user command inquiry
    # specified commands are executed as required
    user_command = input("Spot Cleaning or General Cleaning (S/G): ") if not command_cycle else "proceed"
    spot_clean = True if user_command == 'S' or user_command == 's' or spot_clean else False
    gen_clean = True if user_command == 'G' or user_command == 'g' or gen_clean else False

    # TREE EVALUATION
    # tree evaluated on every new command cycle interaction with the user
    if not command_cycle:
        b_tree = tree_root.run(current_blackboard)

    # spot cleaning command
    if spot_clean:
        if current_blackboard.get_in_environment(BATTERY_LEVEL, 0) > 30:
            current_blackboard.set_in_environment(SPOT_CLEANING, True)
            tree = tree_root.run(current_blackboard)
            spot_cycle = spot_cycle + 1
            if spot_cycle == 20:
                current_blackboard.set_in_environment(TIMER, 0)
                tree = tree_root.run(current_blackboard)
                task_done = True
                spot_cycle = 0
        else:
            low_battery = battery_seq.run(current_blackboard)

    # general cleaning command
    if gen_clean:
        # check for battery. If lower than 30 make way to charging, then resume general cleaning
        if current_blackboard.get_in_environment(BATTERY_LEVEL, 0) > 30:
            current_blackboard.set_in_environment(GENERAL_CLEANING, True)

            # tree evaluation for general cleaning
            # checks if dusty_spot was true and conduct 35s of spot cleaning
            tree = tree_root.run(current_blackboard)

            if dusty_spot:
                spot_cycle = spot_cycle + 1
                if spot_cycle == 35:
                    current_blackboard.set_in_environment(TIMER, 0)
                    tree = tree_root.run(current_blackboard)
                    task_done = True
                    spot_cycle = 0

        else:
            low_battery = battery_seq.run(current_blackboard)

    # determining solution termination
    if task_done or spot_cycle == 0:
        done = True
        sensor_cycle = 0
    else:
        done = False

    # update command cycle after each loop completion
    command_cycle = True
