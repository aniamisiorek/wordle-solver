# 5 letter word to be guessed
# Green, yellow and gray as feedback ( 0 - green, 1 - yellow, 2 - grey )
# We should keep track of letters and the color feedback received
# Store previously used letters with associated feedback and position

# State represented by word + feedback + position for every letter in the word: [('a', 0, 2), ('i', 0, 2), ('r', 0, 2)]
# We pass a tuple with (new state: [('b', 1, 0), ('a', 1, 1), ('r', 1, 2)], visited letters: [['t', 2, 0], ['x', 1, 1]], cost of word: 4)
import heapq


def load_solutions():
    with open('wordle_solutions.txt') as solution_file:
        solutions = set(solution_file.read().split())
    return solutions

class Search:

    # constructor: tuple with input[0] being a string that represents a guess
    #                         input[1] being the feedback for this guess

    # state: word descriptor(described below), set of used words, set of used letters
    # word descriptor: for 'catch', [0 1 2 0 1] -> ('c', 0, 0), ('a', 1, 1), ('t', 2, 2), ('c', 0, 3), ('h', 1, 4)
    def __init__(self, word):
        self.solutions = set(load_solutions())
        # initial word is "catch" with everything greyed out
        # self.initialState = 'catch', ('c', 2, 0), ('a', 2, 1), ('t', 2, 2), ('c', 2, 3), ('h', 2, 4),
        #                      set('catch'), set('c', 'a', 't', 'h')
        self.initial_state = self.create_word(word[0], word[1], set(word[2]), set())

    # input will be a word followed by the feedback in the same format
    def create_word(self, word, feedback, used_words, used_letters):
        word_descriptor = []
        # add the word to the used words
        used_words.add(word)
        for position in range(0, len(word)):
            result = word[position], feedback[position], position
            word_descriptor.append(result)
            # added grayed out letters to the used letters
            if feedback[position] == 2:
                used_letters.add(word[position])
            elif feedback[position] == 1 or feedback[position] == 0:
                if used_letters.__contains__(word[position]):
                    used_letters.remove(word[position])
        return word, word_descriptor, used_words, used_letters

    # checks to see if a possible solution matches with a word descriptor, green should exist in green and yellow
    # should not be in the same spot
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

    """ Returns a list of words from the solution set that match the given constraints.
    Match green letters, use yellow letters and avoid grey letters.
    """
    def get_successor(self, parent_state):
        successors = []
        for possible_solution in self.solutions:
            new_state = self.check_word(possible_solution, parent_state)
            if new_state is not None:
                successors.append(new_state)
        return successors

    def ucs_result(self):
        path = self.uniform_cost_search()
        return path[0]

    def uniform_cost_search(self):
        """Search the node of least total cost first."""
        initial_state = self.initial_state
        frontier = PriorityQueue()
        frontier.push((initial_state, [], 0), 0)
        explored = []

        while not frontier.isEmpty():
            state, path, total_cost = frontier.pop()
            while state in explored:
                state, path, total_cost = frontier.pop()
            explored.append(state)
            successors = self.get_successor(state)
            if len(successors) == 0:
                return path
            for new_word in successors:
                next_cost = total_cost + 1
                next_node = new_word, list(path) + [new_word[0]], next_cost
                if new_word[0] not in explored:
                    frontier.push(next_node, next_cost)


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