# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "clean_spot" task of the behavior tree

import bt_library as btl
import bt as bt
from ..globals import SPOT_CLEANING, TIMER


class CleanSpot(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Spot Cleaning in Progress")

        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(TIMER, 0) == 0 \
            else self.report_running(blackboard)
