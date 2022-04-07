# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ucs import Search

def return_name():
    search = Search(('catch', [2, 2, 2, 2, 2]))
    return search.uniformCostSearch()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(return_name())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
