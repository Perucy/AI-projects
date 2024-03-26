# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "done general" task of the behavior tree
import bt as bt
import bt_library as btl
from ..globals import GENERAL_CLEANING, CLEAN_FLOOR, DUSTY_SPOT_SENSOR


class DoneGeneral(btl.Task):
    def run(self,blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Clear general")

        clean = blackboard.get_in_environment(CLEAN_FLOOR, False)
        dustless = blackboard.get_in_environment(DUSTY_SPOT_SENSOR, False)

        if clean or dustless:
            blackboard.set_in_environment(GENERAL_CLEANING, False)
            blackboard.set_in_environment(DUSTY_SPOT_SENSOR, False)

        # return success when GENERAL_CLEANING is false, failed otherwise
        return self.report_succeeded(blackboard) \
            if not blackboard.get_in_environment(GENERAL_CLEANING, False) \
            else self.report_failed(blackboard)
