# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "do nothing" task of the behavior tree
import bt_library as btl
import bt as bt
from ..globals import SPOT_CLEANING, GENERAL_CLEANING, BATTERY_LEVEL


class DoNothing(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Do Nothing")

        # return success the robot is not cleaning or docking, failure otherwise
        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(BATTERY_LEVEL, 0) > 30 \
            and not blackboard.get_in_environment(SPOT_CLEANING, False) \
            and not blackboard.get_in_environment(GENERAL_CLEANING, False) \
            else self.report_failed(blackboard)
