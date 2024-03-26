# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "Go Home" task of the behavior tree
import bt_library as btl
import bt as bt
from ..globals import HOME_PATH


class GoHome(btl.Task):
    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:
        self.print_message("Going Home")
        
        self.print_message("Up Left Left Up Right")
        
        return self.report_succeeded(blackboard)