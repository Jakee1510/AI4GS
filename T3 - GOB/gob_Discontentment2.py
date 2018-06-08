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
goals = {
    'Eat': 4,
    'Sleep': 3,
    'Toilet': 2,
}

# Global (read-only) actions and effects
actions = {
    'get raw food': { 'Eat': -2, 'Toilet': +2},
    'get snack': { 'Eat': -1, 'Toilet': +1},
    'sleep in bed': { 'Sleep': -4 },
    'go to the toilet': { 'Toilet': -3 }
}


def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in list(actions[action].items()):
        goals[goal] = max(goals[goal] + change, 0)



    
def getDiscontent(newValue):
    
    return newValue * newValue

    
def calcDiscontent(action, goals):

    discontent = 0

    for key, value in actions[action].items():
        newValue = value + goals[key]
        discontent += getDiscontent(newValue)

    return discontent


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
##        print("TRUE")
        return -sum(actions[action].values())
        
    else:
        # It isn't, so utility is zero.
##        print("FALSE")
        return 0



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
    best_action = 'go to the toilet'
    best_value = calcDiscontent(best_action, goals)
    thisValue = None
    
    for key, value in actions.items():
        thisValue = calcDiscontent(key, goals)
        print("DISCONTENTMENT FOR", key, ":", thisValue)
        if thisValue < best_value:
            best_value = thisValue
            best_action = key

    return best_action


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
        print('GOALS:', goals)
        # What is the best action
        action = choose_action()
        print('BEST ACTION:', action)
        # Apply the best action
        apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in list(goals.items())):
            running = False
        print(HR)
    # finished
    print('>> Done! <<')

if __name__ == '__main__':
    run_until_all_goals_zero()
