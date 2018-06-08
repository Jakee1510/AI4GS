from time import sleep
from copy import deepcopy
import itertools
'''Goal Oriented Behaviour

Clinton Woodward, 2015, cwoodward@swin.edu.au
Works with Python 3+

Please don't share this code without permission.

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''
VERBOSE = True

# Global goals with initial values


costs = {

    'Energy': 5

}

goals = {
    'Heal': 4,
    'Kill-Ogre': 3,
}

# Global (read-only) actions and effects
actions = {
    'Lesser-Healing': {'Heal': -2, 'Kill-Ogre': -0, 'Energy': -2},
    'Fireball': { 'Heal': +0, 'Kill-Ogre': -2, 'Energy': -3},
    'Greater-Healing': { 'Heal': -4, 'Kill-Ogre': -0, 'Energy': -3},



}


def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''

    '''I've had to use exceptions to allow the use of costs and goal changes
        It's probably not the most elegant method, but it works    
    '''
    for goal, change in list(actions[action].items()):
        isDiscontentment = True
        try:
            goals[goal]
        except KeyError:
            isDiscontentment = False
        if isDiscontentment:
            goals[goal] = max(goals[goal] + change, 0)

        isCost = True
        try:
            costs[goal]
        except KeyError:
            isCost = False
        if isCost:
            costs[goal] = max(costs[goal] + change, 0)





    
def getDiscontent(newValue):
    return newValue * newValue

    
def calcDiscontent(action, goals2):

    discontent = 0

    for key, value in actions[action].items():
        isDiscontent = True
        try:
            goals[key]
        except KeyError:
            isDiscontent = False
        if isDiscontent:
            newValue = value + goals2[key]
            discontent += getDiscontent(newValue)

    return discontent


def calcCost(action):

    cost = 0

    for key, value in actions[action].items():
        isCost = True
        try:
            costs[key]
        except KeyError:
            isCost = False
        if isCost:
            newValue = value + costs[key]
            cost = newValue

    return cost


def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".

    For example::
        action_utility('get raw food', 'Eat')

    returns a number representing the effect that getting raw food has on our
    'Eat' goal. Larger (more positive) numbers mean the action is more
    beneficial.
    '''
    ### Simple version - the utility is the change to the specified goal

    if goal in actions[action]:
        # Is the goal affected by the specified action?
        return -sum(actions[action].values())
        
    else:
        # It isn't, so utility is zero.
        return 0



def discontentment(goalsz):
    discontent = 0

    for key, value in goals.items():
        isDiscontent = True
        try:
            goals[key]
        except KeyError:
            isDiscontent = False
        if isDiscontent:
            newValue = value
            discontent += getDiscontent(newValue)


    return discontent



class State(object):
    def __init__(self, actionss, goalss=None, costss=None):
        self.goals = deepcopy(goalss) if goalss else goals
        self.actions = actionss
        self.costs = deepcopy(costss) if costss else costs
        self.iter = 0
        self._current_actions = [action for name, action in list(self.actions.items())]
        self.depth = 0
        self.bestdiscontentment = None
        self.bestplan = []


    def discontentment(self):
        discontent = 0

        for key, value in self.goals.items():
            isDiscontent = True
            try:
                self.goals[key]
            except KeyError:
                isDiscontent = False
            if isDiscontent:
                newValue = value
                discontent += getDiscontent(newValue)
        return discontent

    def world_apply_action(self, action, goals2=None, costs2=None):

        worldgoals = goals2 if goals2 else deepcopy(self.goals)
        worldcosts = costs2 if costs2 else deepcopy(self.costs)

        for goal, change in list(self.actions[action].items()):
            isDiscontentment = True
            try:
                worldgoals[goal]
            except KeyError:
                isDiscontentment = False
            if isDiscontentment:

                worldgoals[goal] = max(self.goals[goal] + change, 0)
                if self.depth == 0:
                    self.goals[goal] = worldgoals[goal]
                print(goal, change)
                print("Goal STATS:", change, "of GOAL", worldgoals, self.goals)



            isCost = True
            try:
                worldcosts[goal]
            except KeyError:
                isCost = False
            if isCost:

                worldcosts[goal] = self.costs[goal] + change
                if self.depth == 0:
                    self.costs[goal] = worldcosts[goal]

                self.depth += 1


                print("Energy CHANGE:", change, "of GOAL", worldcosts, self.costs)


        return worldgoals, worldcosts



    def apply_action_reset(self, action):
        self.world_apply_action(action)
        self._current_actions = self.valid_actions()

        self._valid_action_len = len(self._current_actions)



    def get_next_action(self, doiter=True):

        try:
            next_index = list(self.actions).pop(self.iter)
            print(list(self.actions)[self.iter], calcDiscontent(list(self.actions)[self.iter], self.goals))

            # print(next_index, "NEXT_INDEX")
        except IndexError:
            self.iter = 1
            return None


        self.iter += 1


        return next_index



    def try_action(self, action):

        goals2 = deepcopy(self.goals)
        costs2 = deepcopy(self.costs)

        return self.world_apply_action(action, goals2, costs2)



    def valid_actions(self):
        theseactions = []

        tempdisc = 10000

        #If a valid action, store it into the best path.
        for name, action in self.actions.items():

            goals2, costs2 = self.try_action(name)
            print("-----------------------------------------")
            print(name, calcDiscontent(name, self.goals))
            if all(value >= 0 for key, value in costs2.items()):
                if calcDiscontent(name,self.goals) < tempdisc:
                    tempdisc = calcDiscontent(name,self.goals)

                    theseactions.append((name))
                    self.bestplan.append((name))
            else:
                print("Cannot perform action due to lack of Energy")

        self.bestdiscontentment = tempdisc
        self.costs = costs



        # self.goals = goals
        print("THESE ARE THE SUCCESSFUL ACTIONS", theseactions)



        return theseactions




def choose_action_goap(max_depth):


    states = [[State(deepcopy(actions), goals, deepcopy(costs)), list(actions).append('Base')]]

    best_value = 100000
    best_plan = []
    depth = 0

    verbose = True

    if verbose:
        print('Searching.....')

    changed = True


    while states:
        print("===========================================|")
        sleep(0.3)

        current_value = states[-1][0].bestdiscontentment
        if states[-1][0].bestdiscontentment == None:
            current_value = states[-1][0].discontentment()

        if len(states) >= max_depth:

            if current_value < best_value:
                print(current_value, ":CURRENTVALUE")
                print(best_value, "BEST VALUE")

                best_value = current_value

                best_plan = states[-1][0].bestplan
                print(best_plan)


                states[-1][0].goals = goals #PROBLEM
                states[-1][0].depth = 0
                states.pop()

                continue

            else:
                states[-1][0].goals = goals
                states[-1][0].depth = 0

        if (states[-1][0] != None):
            next_action = states[-1][0].get_next_action()

        else:
            states[-1][0] = None


        if next_action:
            new_state = deepcopy(states[-1][0])
            states.append([new_state, None])
            states[-1][1] = next_action
            new_state.apply_action_reset(next_action)

            changed = True


        else:

            states.pop()

    result = best_plan


    return result[0], result[1]





def choose_action():
    '''Return the best action to respond to the current most insistent goal.
    '''
    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'
    
    best_goal = None
    for key, value in goals.items():
        if best_goal is None or value > goals[best_goal]:
           best_goal = key

    if VERBOSE: print('BEST_GOAL:', best_goal, goals[best_goal])


    ### CHOOSE ACTION WITH LOWEST DISCONTENTMENT
    best_action = 'Complete Small Quest'
    best_value = calcDiscontent(best_action)
    thisValue = None
    
    for key, value in actions.items():
        thisValue = calcDiscontent(key)
        thisCost = calcCost(key)

        print("COST FOR PERFORMING:", key, ":", thisCost)
        print("DISCONTENTMENT FOR", key, ":", thisValue)
        if thisValue < best_value:
            best_value = thisValue
            best_action = key

    return best_action


# def choose_action_goap():




#==============================================================================

def print_actions():
    print('ACTIONS:')
    for name, effects in list(actions.items()):
        print(" * [%s]: %s" % (name, str(effects)))

def run_until_all_goals_zero():
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    while running:
        sleep(1.0)
        print('COSTS:', costs)
        print('GOALS:', goals)
        # What is the best action
        action = choose_action_goap(2)

        print('BEST SET OF ACTIONS:', action)
        # Apply the best action

        for i in range(len(action)):
            apply_action((action[i]))
        print('NEW GOALS:', goals)

        # Stop?
        if all(value == 0 for goal, value in list(goals.items())):
            running = False
        if all(value == 0 for goal, value in list(costs.items())):
            running = False
        print(HR)
    # finished
    print('>> Done! <<')

if __name__ == '__main__':
    run_until_all_goals_zero()
