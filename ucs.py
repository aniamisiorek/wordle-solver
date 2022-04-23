# Green, yellow and gray as feedback ( 0 - green, 1 - yellow, 2 - grey )
import heapq


# Loads Wordle solutions from a .txt file into a set
def load_solutions():
    with open('wordle_solutions.txt') as solution_file:
        solutions = set(solution_file.read().split())
    return solutions


# Represents a search problem that describes the game 'Wordle'. Each search problem is initialized with a guess from
# a user. This guess will form the initial state space.
class Search:

    # constructor: tuple with input[0] being a string that represents a guess
    #                         input[1] being the feedback for this guess
    #                         input[2] being the previously used words (to avoid repetition)

    def __init__(self, word):
        self.solutions = set(load_solutions())
        self.initial_state = State((word[0], word[1], set(word[2]), set(self.get_letters(word[2]))))

    def get_letters(self, word_list):
        result = set()
        for word in word_list:
            for letter in word:
                result.add(letter)

        return result

    # Performs uniform cost search on the user's guess, returning the word with the shortest path
    def uniform_cost_search(self):
        initial_state = self.initial_state
        frontier = PriorityQueue()
        frontier.push((initial_state, [], 0), 0)
        explored = []

        while not frontier.isEmpty():
            state, path, total_cost = frontier.pop()
            while state in explored:
                state, path, total_cost = frontier.pop()
            explored.append(state)
            successors = state.get_successors(self)
            if len(successors) == 0:
                return path
            for new_word in successors:
                next_cost = total_cost + 1
                next_node = new_word, list(path) + [new_word.word], next_cost
                if new_word not in explored:
                    frontier.push(next_node, next_cost)

    # Performs A* search on the Wordle state space, returning the word with the shortest path.
    # Uses a heuristic where words with less successors are explored first
    def a_star_search(self):
        initial_state = self.initial_state
        frontier = PriorityQueue()
        frontier.push((initial_state, [], 0), 0)
        explored = []

        while not frontier.isEmpty():
            state, path, total_cost = frontier.pop()
            while state in explored:
                state, path, total_cost = frontier.pop()
            explored.append(state)
            successors = state.get_successors(self)
            if len(successors) == 0:
                return path
            for new_word in successors:
                next_cost = total_cost + 1 + heuristic_successors(successors,self.solutions)
                next_node = new_word, list(path) + [new_word.word], next_cost
                if new_word not in explored:
                    frontier.push(next_node, next_cost)

    # Returns the result from UCS and accounts for mistypes in the user input.
    def ucs_result(self):
        path = self.uniform_cost_search()
        if len(path) == 0:
            return "Could not find valid word! Double check your input."
        else:
            return path[0]

    # Returns the result from A* and accounts for mistypes in the user input.
    def astar_result(self):
        path = self.a_star_search()
        if len(path) == 0:
            return "Could not find valid word! Double check your input."
        else:
            return path[0]


# Represents a state for a Wordle game. A State contains a word in string format, word descriptor(described below),
# set of used words, and a set of used letters'
# word descriptor: for 'catch', [0 1 2 0 1] -> ('c', 0, 0), ('a', 1, 1), ('t', 2, 2), ('c', 0, 3), ('h', 1, 4)
class State:

    def __init__(self, guess):
        state_params = self.create_word(guess[0], guess[1], guess[2], guess[3])
        self.word = state_params[0]
        self.word_descriptor = state_params[1]
        self.used_words = state_params[2]
        self.used_letters = state_params[3]

    # Returns whether two states are equal. A state is equal to another iff they are composed of the same word, have
    # the same feedback, and have the same used words and letters
    def __eq__(self, other):
        return self.word == other.word and self.word_descriptor == other.word_descriptor and \
               self.used_words == other.used_words and self.used_letters == other.used_letters

    # Creates a state for a solution given the word and its feedback. Readjusts the used words and letters accordingly.
    def create_word(self, word, feedback, used_words, used_letters):
        word_descriptor = []

        # make a copy of used letters
        new_used_letters = used_letters.copy()

        # make a copy of used words and add the new word
        new_used_words = used_words.copy()
        new_used_words.add(word)

        # keeps track of not gray letters (green or yellow), so we do not accidentally add letters that are in the
        # word, but are grayed out elsewhere
        not_gray = set()

        for position in range(0, len(word)):
            result = word[position], feedback[position], position
            word_descriptor.append(result)

            # added grayed out letters to the used letters
            if feedback[position] == 2:
                if not not_gray.__contains__(word[position]):
                    new_used_letters.add(word[position])

            if feedback[position] == 1 or feedback[position] == 0:
                not_gray.add(word[position])
                if new_used_letters.__contains__(word[position]):
                    new_used_letters.remove(word[position])

        return word, word_descriptor, new_used_words, new_used_letters

    # Checks to see if a possible solution matches with the constraints set by the parent state. Green letters should
    # exist in both words in the same position, yellow letters should not be in the same spot (but both exist in word),
    # and gray letters should not exist anywhere in solution.
    def check_word(self, possible_solution):

        # checks if word has been used already
        if self.used_words.__contains__(possible_solution):
            return None

        # assume all feedback is grayed out
        new_feedback = [2, 2, 2, 2, 2]

        for i in range(0, len(possible_solution)):
            letter = self.word_descriptor[i]
            # green case
            if letter[1] == 0 and possible_solution[i] != letter[0]:
                return None
            # need to readjust feedback
            elif letter[1] == 0 and possible_solution[i] == letter[0]:
                new_feedback[i] = 0

            # yellow case
            if letter[1] == 1 and possible_solution[i] == letter[0]:
                return None
            elif letter[1] == 1 and possible_solution[i] != letter[0]:
                # seeing if the possible letter exists somewhere else in the possible word
                flag = True
                for j in range(0, len(possible_solution)):
                    if letter[0] == possible_solution[j]:
                        if new_feedback[j] == 2:
                            new_feedback[j] = 1
                            flag = False
                            break
                if flag:
                    return None

            # checking if any letter in possible solution has already been grayed out
            if self.used_letters.__contains__(possible_solution[i]):
                return None

        return State((possible_solution, new_feedback, self.used_words, self.used_letters))

    # Returns a list of successive states/solutions that pass the check_word method.
    def get_successors(self, search_problem):
        successors = []
        for possible_solution in search_problem.solutions:
            new_state = self.check_word(possible_solution)
            if new_state is not None:
                successors.append(new_state)
        return successors


# HEURISTICS #

# Number of repeated letters
def heuristic_counts(w):
    counts = [w.count(i) for i in set(w)]
    h = 0
    for i in counts:
        if i > 1:
            h += 1
    return h


# Numbers of successors
def heuristic_successors(successor_list, solutions_list):
    return len(successor_list)/len(solutions_list)


# Priority Queue data structure used in UCS.
class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
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
