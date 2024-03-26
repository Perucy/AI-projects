# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "dock" task of the behavior tree
import bt_library as btl
import bt as bt
from ..globals import BATTERY_LEVEL


class Dock(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Docking in Progress")

        blackboard.set_in_environment(BATTERY_LEVEL, 100)

        self.print_message("Fully Charged")

        # return success after fully charging
        return self.report_succeeded(blackboard)