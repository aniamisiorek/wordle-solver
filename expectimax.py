# 5 letters, green yellow and gray
# we should keep track of letters that are all colors
# tuple with ([a, 5], [[t, 5], [x, 1]], [q, w, e, r])
import queue


class Search():

    def __init__(self, solutions):
        self.solutions = set(solutions)
        self.solution_set = len(solutions[0])

    """Checks whether a word is valid based on the known conditions of the word"""
    def valid_words(self, word):
        pass

    """Determines the cost of a word, lower cost means this word is better. Words with higher costs are worse.
    We should be picking a word with letters that are contained in as many solutions as possible. For each letter
    shared with other solutions, +1"""
    def word_cost(self, word):
        pass

    def uniformCostSearch(problem):
        """Search the node of least total cost first."""
        "*** YOUR CODE HERE ***"
        initial_state = problem.getStartState()
        frontier = queue.PriorityQueue
        frontier.push(0, (initial_state, [], 0))
        explored = []

        while not frontier.isEmpty():
            state, path, totalCost = frontier.pop()
            while state in explored:
                state, path, totalCost = frontier.pop()
            explored.append(state)
            if problem.isGoalState(state):
                return path
            for neighbor in problem.getSuccessors(state):
                nextCost = totalCost + neighbor[2]
                nextNode = (neighbor[0], list(path) + [neighbor[1]], nextCost)
                if neighbor[0] not in explored:
                    frontier.push(nextNode, nextCost)

