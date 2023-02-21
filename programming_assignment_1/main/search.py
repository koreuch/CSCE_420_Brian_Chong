# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

import heapq

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def heuristic1(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    # print(state)
    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y     = problem.goal
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        optimisitic_number_of_steps_to_goal = 0
        return optimisitic_number_of_steps_to_goal
    # 
    # traveling-salesman problem (collect multiple food pellets)
    # 
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is
        # print(state[1].count())
        # return 0
        # problem.heuristic_info['count'] += 1
        position, food_grid = state
        pacman_x, pacman_y = position
        # travel_spaces = food_grid.width * food_grid.height
        # if (state[1].count() < 25):
        # print(state[1].count())
        # if (problem.heuristic_info['count'] == 200):
        #     print(state[1].count())
        #     print(position)
        #     problem.heuristic_info['count'] = 0
        # print("INFO")
        # print(problem.get_start_state())
        # print(food_grid.width, "Here is the width")
        # print(food_grid.height, "Here is the height")
        # print(food_grid.height / 2, "I can use this for half height")
        # print(food_grid.width / 2, "I can use this for half width")
        # return 0

        pellet_percent = float(state[1].count()) / float(problem.heuristic_info['pellet_count'])
        # print("percentage", pellet_percent)

        # if food_grid[pacman_x][pacman_y]:
        #     # print("found here", food_grid[pacman_x][pacman_y])
        #     return state[1].count() - 1
        # elif food_grid[pacman_x-1][pacman_y] or food_grid[pacman_x+1][pacman_y] or food_grid[pacman_x][pacman_y-1] or food_grid[pacman_x][pacman_y+1]:
        #     return state[1].count()
        # else:
        #     return state[1].count() + 1\

        return (food_grid.width * food_grid.height * pellet_percent)
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        optimisitic_number_of_steps_to_goal = 0
        return optimisitic_number_of_steps_to_goal



#   
    # transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # start_state = problem.get_start_state()
    # transitions = problem.get_successors(start_state)
    # print("These are the transitions")
    # for transition in transitions:
    #     print("Transition:")
    #     print(transition)
    # print("\nThese are the start state printed out")
    # print(start_state)
    # # Example:
    # #     start_state = problem.get_start_state()
    # #     transitions = problem.get_successors(start_state)
    # #     example_path = [  transitions[0].action  ]
    # #     path_cost = problem.get_cost_of_actions(example_path)
    # #     return example_path
    # heuristic(problem)
    # util.raise_not_defined()
    #
    #above is notes for a star
def a_star_search(problem, heuristic=heuristic1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # problem.heuristic_info['count'] = 1
#state[1].count()
    start_state = problem.get_start_state() # returns a string
    start_node = {"state": start_state, "cost":0, "sequence": [] }
    # print(str(problem))
    # print("used this")
    #base case above
    frontier = []
    entry_count = 0 # priorities that are equal will lead to error with heapq. This mitigates that

    #This was for the test cases, since the food search problem I use problem.heuristic_info dictionary
    if (str(type(problem)) == "<class \'search_agents.FoodSearchProblem\'>"):
        pellet_count = (problem.get_successors(start_state))[0].state[1].count()
        # print("here it is")
        # print(type(problem))
        problem.heuristic_info['pellet_count'] = pellet_count

    heapq.heappush(frontier, (0, entry_count, start_node))
    explored = {}
    entry_count += 1
    explored[start_node["state"]] = 0
    depth = 1
    exploredNodes = []
    while len(frontier) != 0:
        node = frontier[0][2]
        # print("Exploring node", node["state"], " with cost: ", frontier[0][0])
        # print(frontier)
        heapq.heappop(frontier)
        if problem.is_goal_state(node["state"]):
            return node["sequence"]

        transitions = problem.get_successors(node["state"])
        for transition in transitions:
            child_node = {"state": transition.state, "cost": node["cost"] + transition.cost, "sequence": node["sequence"] + [transition.action] }
            # if (transition.state) in explored:
            if (transition.state not in explored) or (explored[transition.state] > child_node["cost"]):

                # print("adding to frontier: ", (node["cost"] + 1), "for state", child_node["state"])

                #for the push, we apply the heuristic for prioirty
                heapq.heappush(frontier, (child_node["cost"] + heuristic(child_node["state"], problem), entry_count, child_node))
                entry_count += 1
                explored[transition.state] = child_node["cost"]
        # print(len(frontier))
    print("This part shouldn't be reached")
    return []


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search