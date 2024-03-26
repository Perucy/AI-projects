# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "spot cleaning" condition of the behavior tree

import bt_library as btl
from ..globals import SPOT_CLEANING


class SpotCleaning(btl.Condition):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Checking for Spot Cleaning")

        # return success when the state of SPOT_CLEANING is True, failure otherwise
        return self.report_failed(blackboard) \
            if not blackboard.get_in_environment(SPOT_CLEANING, False) \
            else self.report_succeeded(blackboard)
