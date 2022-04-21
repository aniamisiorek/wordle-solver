from ucs import Search, State, load_solutions
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


# Returns the best word from UCS.
def return_word():
    # running our algorithm on blank input returns 'prude', therefore we will use this word
    search = Search(('11111', [2, 2, 2, 2, 2], []))
    return search.astar_result()

# Starts a Wordle game that is operated by UCS
def start_game_ucs():
    print('Welcome to Wordle!')
    user_keep = 'yes'
    i = 1
    used_words = []
    while user_keep.lower() != 'no':
        a = 'Attempt ' + str(i) + ', enter your guess: '
        user_input = str(input(a))
        user_feedback = [int(item) for item in input("Enter the feedback values: ").split()]
        search = Search((user_input, user_feedback, used_words))
        print('Try: ', search.ucs_result())
        user_keep = str(input('Do you want to keep playing?: '))
        used_words.append(user_input)
        i += 1

# Starts a Wordle game that is operated by A*
def start_game_astar():
    print('Welcome to Wordle!')
    user_keep = 'yes'
    i = 1
    used_words = []
    while user_keep.lower() != 'no':
        a = 'Attempt ' + str(i) + ', enter your guess: '
        user_input = str(input(a))
        user_feedback = [int(item) for item in input("Enter the feedback values: ").split()]
        search = Search((user_input, user_feedback, used_words))
        print('Try: ', search.astar_result())
        user_keep = str(input('Do you want to keep playing?: '))
        used_words.append(user_input)
        i += 1

    print('Well done! See u at the next game :)')

# Gets the feedback for a guess according to the passed solution. IN PROGRESS
def get_feedback(guess, solution):
    fb = [2,2,2,2,2]
    for i in range(len(guess)):
        if guess[i] in solution:
            fb[i] = 1
        if guess[i] == solution[i]:
            fb[i] = 0
    return fb

# Runs a test on both UCS and A* to compare the efficiency of the search functions
def test(iterations):
    solution_set = list(load_solutions())
    results_ucs = []
    results_astar = []
    #s = Search(('11111', [2, 2, 2, 2, 2], []))
    #guess_ucs = s.ucs_result()
    for i in range(iterations):
        guess_ucs = 'start'
        print('guess 1 ucs', guess_ucs)
        used_words = []
        solution_word = random.choice(solution_set)
        print('solution',solution_word)
        attempt = 1
        while guess_ucs != solution_word:
            attempt += 1
            print('attempt ucs', attempt)
            if attempt == 7:
                break
            feedback = get_feedback(guess_ucs, solution_word)
            search = Search((guess_ucs, feedback, used_words))
            guess_ucs = search.ucs_result()
            if guess_ucs == 'Could not find valid word! Double check your input.':
                attempt = 0
                break
            print('guess: ',guess_ucs)
            used_words.append(guess_ucs)

        results_ucs.append(attempt)
        # for astar
        # guess_astar = s.astar_result()
        guess_astar = 'start'
        print('guess  1 astar', guess_astar)
        used_words = []
        attempt = 1
        while guess_astar != solution_word:
            if attempt == 7:
                break
            feedback = get_feedback(guess_astar, solution_word)
            search = Search((guess_astar, feedback, used_words))
            guess_astar = search.astar_result()
            if guess_astar == 'Could not find valid word! Double check your input.':
                attempt = 0
                break
            print('guess: ', guess_astar)
            used_words.append(guess_astar)
            print('attempt astar', attempt)
            attempt += 1
        results_astar.append(attempt)

    return results_ucs, results_astar

# Creates a graph representing the distribution of UCS and A* search
def plot_distributions(ucs, astar, iterations):
    sns.set_style("white")

    labels = ['UCS']*iterations + ['A*']*iterations

    data = pd.DataFrame(list(zip(labels, ucs+astar)), columns = ['algorithm', 'attempt'])

    sns.displot(data, x='attempt', hue='algorithm',alpha=0.4, fill=True, aspect=1.5)
    plt.xlabel('Attempt')
    plt.ylabel('Count')
    plt.title('Distribution of correct guesses')
    plt.xticks([0,1,2,3,4])
    plt.show()

# Main function
if __name__ == '__main__':
    #print(return_word())
    #start_game_astar()
    results_ucs, results_astar = test(20)
    print('ucs: ',results_ucs)
    print('astar: ',results_astar)
    ucs = [2,3,4,3,1,3,1,2]
    astar = [0, 2, 1, 3, 1, 3, 1, 2]
    plot_distributions(results_ucs, results_astar, len(results_astar))
