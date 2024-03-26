# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "always fail" task of the behavior tree
import bt as bt
import bt_library as btl
from ..globals import DUSTY_SPOT_SENSOR


class AlwaysFail(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        self.print_message("Dusty spot clean")

        # return success when dusty_spot_sensor is true, failure otherwise
        return self.report_succeeded(blackboard) \
            if blackboard.get_in_environment(DUSTY_SPOT_SENSOR, False) \
            else self.report_failed(blackboard)
