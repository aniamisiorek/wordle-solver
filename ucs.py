# Green, yellow and gray as feedback ( 0 - green, 1 - yellow, 2 - grey )
# We should keep track of letters and the color feedback received
# Store previously used letters with associated feedback and position
import heapq


# Loads Wordle solutions from a .txt file into a set
def load_solutions():
    with open('wordle_solutions.txt') as solution_file:
        solutions = set(solution_file.read().split())
    return solutions


# Represents a search problem that describes the game 'Wordle'. Each instance is initialized with the guess from a user.
class Search:

    # constructor: tuple with input[0] being a string that represents a guess
    #                         input[1] being the feedback for this guess

    # state: word in string format, word descriptor(described below), set of used words, set of used letters'
    # word descriptor: for 'catch', [0 1 2 0 1] -> ('c', 0, 0), ('a', 1, 1), ('t', 2, 2), ('c', 0, 3), ('h', 1, 4)
    def __init__(self, word):
        self.solutions = set(load_solutions())
        self.initial_state = self.create_word(word[0], word[1], set(word[2]), set())

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
    def check_word(self, possible_solution, parent_state):

        # checks if word has been used already
        if parent_state[2].__contains__(possible_solution):
            return None

        # assume all feedback is grayed out
        new_feedback = [2, 2, 2, 2, 2]

        for i in range(0, len(possible_solution)):
            letter = parent_state[1][i]
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
            if parent_state[3].__contains__(possible_solution[i]):
                return None

        new_state = self.create_word(possible_solution, new_feedback, parent_state[2], parent_state[3])
        return new_state

    # Returns a list of successive states/solutions that pass the check_word method.
    def get_successor(self, parent_state):
        successors = []
        for possible_solution in self.solutions:
            new_state = self.check_word(possible_solution, parent_state)
            if new_state is not None:
                successors.append(new_state)
        return successors

    # Performs uniform cost search on the Wordle state space.
    def uniform_cost_search(self):
        initial_state = self.initial_state
        frontier = PriorityQueue()
        frontier.push((initial_state, [], 0), 0)
        print(initial_state)

        while not frontier.isEmpty():
            state, path, total_cost = frontier.pop()
            successors = self.get_successor(state)
            if len(successors) == 0:
                return path
            for new_word in successors:
                next_cost = total_cost + 1
                next_node = new_word, list(path) + [new_word[0]], next_cost
                frontier.push(next_node, next_cost)

    # Returns the result from UCS and accounts for mistypes in the user input.
    def ucs_result(self):
        path = self.uniform_cost_search()
        if len(path) == 0:
            return "Could not find valid word! Double check your input."
        else:
            return path[0]


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
