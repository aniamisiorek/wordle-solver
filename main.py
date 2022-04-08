from ucs import Search

def return_word():
    search = Search(('kayak', [2, 2, 1, 0, 2], ['munch', 'seize']))
    return search.ucs_result()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(return_word())

