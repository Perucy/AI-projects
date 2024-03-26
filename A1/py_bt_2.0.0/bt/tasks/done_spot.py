# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "Done Spot" task of the behavior tree
import bt_library as btl
import bt as bt
from ..globals import SPOT_CLEANING


class DoneSpot(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Clear Spot")

        blackboard.set_in_environment(SPOT_CLEANING, False)

        # return success when SPOT_CLEANING is false, otherwise failed
        return self.report_succeeded(blackboard) \
            if not blackboard.get_in_environment(SPOT_CLEANING, False) \
            else self.report_failed(blackboard)
