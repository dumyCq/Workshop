# search.py

import util

class SearchProblem:

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def IDeepSearch(problem):
    # using data structure "stack" from util
    dfsstack = util.Stack()
    depth = 1
    # save the epoch
    epoch = 0

    while True:
        epoch = epoch + 1
        dfsstack.push((problem.getStartState(), []))
        # save nodes that already visited
        visited = set()
        while not dfsstack.isEmpty():
            node, actions = dfsstack.pop()
            if node in visited:
                continue
            else:
                visited.add(node)
            if problem.isGoalState(node):
                print "epoch: " + str(epoch)
                print "num of nodes: " + str(len(visited))
                return actions
            if len(actions) == depth:
                continue

            for coord, direction, steps in problem.getSuccessors(node):
                dfsstack.push((coord, actions + [direction]))
        # memory = memory + len(visited)
        depth = depth + 1

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # using the data structure "queue" from util
    bfsqueue = util.Queue()
    bfsqueue.push( (problem.getStartState(), []) )
    # the second [] hold the route from startnode to the current node
    visited = set()
    while not bfsqueue.isEmpty():
        node, actions = bfsqueue.pop()
        if node in visited:
            continue
        else:
            visited.add(node)
        if problem.isGoalState(node):
            print "num of nodes: " + str(len(visited))
            return actions
        for coord, direction, steps in problem.getSuccessors(node):
            if not coord in visited:
                bfsqueue.push((coord, actions + [direction]))
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # prior represent the cost from the start node to the current node
    ucfPriorQueue = util.PriorityQueue()
    # two priorQueue to hold node and action
    ucfPriorQueue.push( (problem.getStartState(), []), 0)
    visited = set()

    while not ucfPriorQueue.isEmpty():
        node, actions = ucfPriorQueue.pop()
        if node in visited:
            continue
        else:
            visited.add(node)
        if problem.isGoalState(node):
            print "num of nodes: " + str(len(visited))
            return actions

        for coord, direction, steps in problem.getSuccessors(node):
            new_actions = actions + [direction]
            ucfPriorQueue.push((coord, new_actions), problem.getCostOfActions(new_actions))

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    # print problem.getHeuristic(state)
    # return 0
    return problem.getHeuristic(state)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    closedset = set()
    aStartPriorQueue = util.PriorityQueue()
    start = problem.getStartState()
    # the two PriorQueue hold node and action
    aStartPriorQueue.push( (start, []), heuristic(start, problem))
    # i = 1

    while not aStartPriorQueue.isEmpty():
        # print "epoch: " + str(i)
        node, actions = aStartPriorQueue.pop()
        if node in closedset:
            continue
        else:
            closedset.add(node)
        if problem.isGoalState(node):
            print "num of nodes: " + str(len(closedset))
            return actions
        for coord, direction, cost in problem.getSuccessors(node):
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                aStartPriorQueue.push( (coord, new_actions), score)
        # i += 1

    return []

def IDaStarSearch(problem, heuristic=nullHeuristic):
    dfsstack = util.Stack()
    start = problem.getStartState()
    limit = heuristic(start, problem)
    # save the num of nodes
    memory = 0
    # save the epoch
    epoch = 0

    while True:
        epoch = epoch + 1
        # print "limit: " + str(limit)
        dfsstack.push([problem.getStartState(), [], heuristic(start, problem)])
        visited = set()
        over = set()
        while not dfsstack.isEmpty():
            node, actions, score = dfsstack.pop()
            if node in visited:
                continue
            else:
                visited.add(node)
            if problem.isGoalState(node):
                memory = len(visited)
                print "epoch: " + str(epoch)
                print "num of nodes: " + str(memory)
                return actions
            if score > limit:
                over.add(score)
                continue

            for coord, direction, steps in problem.getSuccessors(node):
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                dfsstack.push([coord, actions + [direction], score])
                # print "score: " + str(score)
        # memory = memory + len(visited)
        limit = min(over)

    return []

def RBFS_Search(problem, heuristic=nullHeuristic):
    closedset = set()
    aStartPriorQueue = util.PriorityQueue()
    start = problem.getStartState()
    # the two PriorQueue hold node and action
    grade = heuristic(start, problem)
    aStartPriorQueue.push([start, [], grade], grade)
    # i = 1
    # save the num of nodes
    memory = 0

    while not aStartPriorQueue.isEmpty():
        # print "epoch: " + str(i)
        node, actions, grade = aStartPriorQueue.pop()
        if aStartPriorQueue.isEmpty():
            second_grade = 10000
        else:
            second_node, second_actions, second_grade = aStartPriorQueue.pop()
            aStartPriorQueue.push([second_node, second_actions, second_grade], second_grade)

        if node in closedset:
            continue
        else:
            closedset.add(node)
        if problem.isGoalState(node):
            print "num of nodes: " + str(memory + len(closedset))
            return actions

        scores = set()
        for coord, direction, cost in problem.getSuccessors(node):
            new_actions = actions + [direction]
            score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
            scores.add(score)
        minscore = min(scores)
        if minscore <= second_grade:
            for coord, direction, cost in problem.getSuccessors(node):
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                aStartPriorQueue.push([coord, new_actions, score], score)
        else:
            aStartPriorQueue.push([node, actions, minscore], minscore)
            # memory = memory + len(scores)



        # i += 1

    return []


