from ucs import Search


# Returns the best word from UCS.
def return_word():
    # running our algorithm on blank input returns 'prude', therefore we will use this word
    search = Search(('liary', [1,0,1,1,2]))
    return search.ucs_result()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(return_word())
