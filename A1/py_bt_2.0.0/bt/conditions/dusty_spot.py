# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "dusty_spot" condition of the behavior tree
import bt_library as btl
from ..globals import DUSTY_SPOT_SENSOR


class DustySpot(btl.Condition):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Checking for Dusty Spot")

        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(DUSTY_SPOT_SENSOR, False) \
            else self.report_failed(blackboard)