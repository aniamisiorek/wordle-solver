from ucs import Search

def return_word():
    search = Search(('soapy', [2, 0, 1, 2, 0], ['adieu']))
    return search.ucs_result()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(return_word())

