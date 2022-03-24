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

    def __init__(self, word):
        self.solutions = set(load_solutions())
        # initial word is "catch" with everything greyed out
        self.initialState = [('c', 2, 0), ('a', 2, 1), ('t', 2, 2), ('c', 2, 3), ('h', 2, 4),
                             set('catch'), set('c', 'a', 't', 'c', 'h')]

    """Goal test: Checks whether a word is valid based on the known conditions of the word"""
    def valid_word(self, state):
        counter = 0
        for i in range(len(state[0])):
            if i[0] == 0:
                counter += 1
        if counter == 3:
            return True
        return False

    # checks to see if a possible solution matches with a word descriptor, green should exist in green and yellow should not be in the same spot
    def check_word(self, word_descriptor, possibleSolution, parentState):
        # checks if word has been used already
        if possibleSolution in parentState[1]:
            return False
        # checks if letter in possible solution is already used in parent and therefore must be discarded
        for letter in possibleSolution:
            if letter in parentState[2]:
                return False
        # check if green is in correct spot
        for letter in range(0, len(possibleSolution)):
            if parentState[0][letter][1] == 2:

    # input will be a word followed by the feedback in the same format
    def create_word(word, feedback):
        # word = 'catch'
        # feedback = [2 2 2 2 2]
        word_descriptor = []
        for position in range(0, len(word)):
            result = word[position], feedback[position], position
            word_descriptor.append(result)
        return word_descriptor

    """Determines the cost of a word, lower cost means this word is better. Words with higher costs are worse.
    We should be picking a word with letters that are contained in as many solutions as possible. For each letter
    shared with other solutions, +1"""
    def word_cost(self, word):
        return 1

    """ Returns a list of words from the solution set that match the given constraints.
    Match green letters, use yellow letters and avoid grey letters.
    """
    def get_successor(self, word_descriptor):
        successors = []
        for possibleSolution in self.solutions:
            if check_word(word_descriptor, possibleSolution):
                successors.append(possibleSolution)
        return successors

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

