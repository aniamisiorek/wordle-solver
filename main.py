from ucs import Search, State


# Returns the best word from UCS.
def return_word():
    # running our algorithm on blank input returns 'prude', therefore we will use this word
    search = Search(('piper', [2, 2, 2, 0, 0], []))
    return search.ucs_result()


def start_game():
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

    print('Well done! See u at the next game :)')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(return_word())
    start_game()
