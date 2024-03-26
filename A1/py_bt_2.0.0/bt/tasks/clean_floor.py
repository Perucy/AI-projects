# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "Clean_Floor" task of the behavior tree
import bt as bt
import bt_library as btl
from ..globals import GENERAL_CLEANING, CLEAN_FLOOR
import random


class CleanFloor(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Cleaning the floor")

        # random generate numbers for the task
        number = random.uniform(0.1, 1.0)

        # initiating the clean floor task
        if number < 0.2:
            blackboard.set_in_environment(CLEAN_FLOOR, True)

        # return success if the number is less than 0.2, running otherwise
        return self.report_succeeded(blackboard) \
            if number < 0.2 \
            else self.report_running(blackboard)

