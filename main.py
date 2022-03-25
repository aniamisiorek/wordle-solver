# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
from expectimax import Search

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def driver():

    valid_solutions = pd.read_csv('data/valid_solutions.csv')
    solution_set = valid_solutions.word.to_list()
    return solution_set
# comment

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(driver())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
