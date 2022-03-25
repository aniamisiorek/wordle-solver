# 5 letter word to be guessed
# Green, yellow and gray as feedback ( 0 - green, 1 - yellow, 2 - grey )
# We should keep track of letters and the color feedback received
# Store preciously used letters with associated feedback and position

# State represented by word + feedback + position for every letter in the word: [('a', 0, 2), ('i', 0, 2), ('r', 0, 2)]
# We pass a tuple with (new state: [('b', 1, 0), ('a', 1, 1), ('r', 1, 2)], visited letters: [['t', 2, 0], ['x', 1, 1]], cost of word: 4)
import queue
import heapq

def load_solutions():
    with open('wordle_solutions.txt') as solution_file:
        solutions = set(solution_file.read().split())
    return solutions

class Search:

    def __init__(self, word):
        self.solutions = set(load_solutions())
        # For 5 letters
        # initial word is "catch" with everything greyed out
        # self.initialState = [('c', 2, 0), ('a', 2, 1), ('t', 2, 2), ('c', 2, 3), ('h', 2, 4),
        #                      set('catch'), set('c', 'a', 't', 'c', 'h')]
        # For 3 letters
        # initial word is "cat" with everything greyed out
        self.initialState = self.create_word('cat', [2, 2, 2])

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
    def check_word(self, possibleSolution, parentState, matches):
        # checks if word has been used already
        if possibleSolution == self.join_word(parentState):
            return False
        # First obtain green matches from all matches (could be yellow or green)
        green = []
        for i in matches:
            if i[2] == 0:
                green.append(i)
        green_letters = self.join_word(green)
        # checks if letter in possible solution is already used in parent but not green and therefore must be discarded
        for letter in possibleSolution:
            if letter in self.join_word(parentState) and letter not in green_letters:
                return False
        # check if green is in correct spot
        # Initialize a counter and look for matches
        counter = 0
        for letter in range(0, len(possibleSolution)):
            if (possibleSolution[letter], 0, letter) in green:
                counter += 1
        # Return True if all greens are in the correct spot
        if counter == len(green):
            return True

    # input will be a word followed by the feedback in the same format
    def create_word(self, word, feedback):
        # word = 'cat'
        # feedback = [2 2 2]
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
    def get_successor(self, parentState, matches):
        successors = []
        for possibleSolution in self.solutions:
            if self.check_word(possibleSolution, parentState, matches):
                successors.append(possibleSolution)
        return successors

    """ Returns the word as a single string for a guess
    """
    def join_word(self, word_descriptor):
        word = []
        for i in word_descriptor:
            word.append(i[0])
        return ''.join(word)

    def uniformCostSearch(self):
        """Search the node of least total cost first."""
        initial_state = self.initialState
        frontier = PriorityQueue()
        frontier.push(0, (initial_state, [], 0))
        explored = []

        while not frontier.isEmpty():
            state, matches, totalCost = frontier.pop()
            while state in explored:
                state, matches, totalCost = frontier.pop()
            explored.append(state)
            if self.valid_word(state):
                return self.join_word(state)
            for neighbor in self.get_successor(state, matches):
                nextCost = totalCost + neighbor[2]
                nextNode = (neighbor[0], list(matches) + [neighbor[1]], nextCost)
                if neighbor[0] not in explored:
                    frontier.push(nextNode, nextCost)



class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)