# CS 131 A1
# Written by: Perucy Mussiba
# Date: 09th February 2024
# Purpose: The code below implements the "priority" composite of the behavior tree

import bt_library as btl


class Priority(btl.Composite):
    def __init__(self, children: btl.NodeListType):
        super().__init__(children)

    def run(self, blackboard: btl.Blackboard) -> btl.ResultEnum:

        running_child = self.additional_information(blackboard, 0)

        for child_position in range(running_child, len(self.children)):
            child = self.children[child_position]

            result_child = child.run(blackboard)

            # return success of the whole composite when a node or child returns success
            if result_child == btl.ResultEnum.SUCCEEDED:
                return self.report_succeeded(blackboard, 0)

            # return running if a child or node is running
            if result_child == btl.ResultEnum.RUNNING:
                return self.report_running(blackboard, child_position)

        # return failure when all children or nodes fail
        return self.report_failed(blackboard, 0)
