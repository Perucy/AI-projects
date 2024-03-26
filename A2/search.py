# CS 131 - Informed search
# Written by: Perucy Mussiba
# Date: 02/24/2024
# Purpose: The file contains an implementation of A* and UC search algorithms for a pancake stack of maximum
#           size 10


import heapq


class Pancakes:
    def __init__(self, stack, a_star, g=0, h=None, flips=None):
        self.stack = stack  # pancake stack
        self.g = g  # backward cost
        self.h = h if h is not None else self.heuristic()  # forward cost
        self.flips = flips if flips else []  # index for flips
        self.a_star = a_star  # bool specifying search algorithm

    def heuristic(self):
        # number of gaps between the pancakes
        return sum(1 for i in range(len(self.stack) - 1) if abs(self.stack[i] - self.stack[i + 1]) > 1)

    def __lt__(self, other):
        # returns true if the total cost of self is less than that of other
        if self.a_star:
            return self.g + self.h < other.g + other.h
        else:
            return self.g < other.g

    def flip_pancakes(self, i):
        # returns new pancake stack after flipping is done
        new_stack = self.stack[i::-1] + self.stack[i + 1:]
        new_flips = self.flips + [i]
        return Pancakes(new_stack, g=self.g + 1, flips=new_flips, a_star=self.a_star)


# main implementation of the algorithms as specified by the user
def pancake_search(stack, a_star):
    # obtaining the goal state of the problem
    goal_state = sorted(stack, reverse=True)

    # initializing the frontier
    frontier = [Pancakes(stack, a_star)]

    # set to keep track of states in the frontier
    frontier_set = {tuple(stack)}

    # set to keep track of visited states
    visited_set = set()

    # dictionary storing the state and its cost
    # for A* search the forward cost(heuristic) is added, in UC the heuristic is ignored and 0 is added instead
    cost = {tuple(stack): frontier[0].g + (frontier[0].h if a_star else 0)}

    # bool to terminate the loop
    done = False

    # loop execution
    while not done:
        # if frontier is empty return failure
        if not frontier:
            return f"FAILURE"

        # obtaining the top state in the frontier and adding it to the visited_set
        node = heapq.heappop(frontier)
        visited_set.add(tuple(node.stack))

        # if the state is the goal state return the solution and print indices representing flip sequences based on
        # the 0-index system
        if node.stack == goal_state:
            done = True
            print("Flip sequences at a 0-based index: ", node.flips)
            print("Sorted pancakes: ")
            return node.stack

        # looping through the children of the node
        for i in range(1, len(node.stack)):
            # flipping the pancakes creating new states
            child = node.flip_pancakes(i)
            # obtaining the cost of each state the forward cost(heuristic) ignored in UC search
            child_cost = child.g + (child.h if a_star else 0)
            # converting the child state into a tuple for comparison
            child_state = tuple(child.stack)

            # checking if the child state in form of a tuple is in the frontier_set or the visited_set
            if child_state not in frontier_set and child_state not in visited_set:
                heapq.heappush(frontier, child)
                frontier_set.add(child_state)
                cost[child_state] = child_cost

            # else if the child state in form of a tuple is in the frontier_set but with a higher cost to
            # be replaced
            elif child_state in frontier_set:
                frontier_child_cost = cost[child_state]
                if child_cost < frontier_child_cost:
                    cost[child_state] = child_cost
                    frontier = list(frontier)
                    frontier = [child if tuple(x.stack) == child_state else x for x in frontier]
                    heapq.heapify(frontier)


# collecting user input about the stack and search algorithm of their preference
stack_search = input("Please enter the pancakes stack separated by spaces (max size 10) to be sorted: ")
stack_list = stack_search.split()
p_stack = [int(num) for num in stack_list]
user_command = input("Select sorting algorithm (A*/UCS). Input A or U respectively: ")
search = True if user_command == "A" else False
print(pancake_search(p_stack, search))
