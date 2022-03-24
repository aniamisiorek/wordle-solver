# 5 letter word to be guessed
# Green, yellow and gray as feedback ( 0 - green, 1 - yellow, 2 - grey )
# We should keep track of letters and the color feedback received
# Store preciously used letters with associated feedback and position

# State represented by letter + feedback + position for every letter in the word: [('a', 0, 2), ('i', 0, 2), ('r', 0, 2)]
# We pass a tuple with (new state: [('b', 1, 0), ('a', 1, 1), ('r', 1, 2)], visited letters: [['t', 2, 0], ['x', 1, 1]], cost of word: 4)
import queue

def load_solutions():
    with open('wordle_solutions.txt') as solution_file:
        solutions = set(solution_file.read().split())
    return solutions


class Search:

    def __init__(self, solutions):
        self.solutions = set(load_solutions())
        self.solution_set = len(solutions[0])

    """Goal test: Checks whether a word is valid based on the known conditions of the word"""
    def valid_word(self, state):
        counter = 0
        for i in range(len(state[0])):
            if i[0] == 0:
                counter += 1
        if counter == 3:
            return True
        return False

    """Determines the cost of a word, lower cost means this word is better. Words with higher costs are worse.
    We should be picking a word with letters that are contained in as many solutions as possible. For each letter
    shared with other solutions, +1"""
    def word_cost(self, word):
        return 1

    """ Returns a list of words from the solution set that match the given constraints.
    Match green letters, use yellow letters and avoid grey letters.
    """
    def get_successor(self, state):
        current_state, visited_set, cost = state

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

