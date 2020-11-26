from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.acquire import get_metadata_cache
from pprint import pprint
from collections import defaultdict 

cache = get_metadata_cache()
#cache.populate()

#cache = get_metadata_cache()

cache.open()
graph = cache.graph

# from gutenberg.query import list_supported_metadatas

# print(get_etexts('author', 'Kipling, Rudyard'))  
# mylist=list(get_etexts('author', 'Kipling, Rudyard'))
# for i in range(0,len(mylist)):
#     print(get_metadata('title', i))

myDict = {
    'Kipling, Rudyard': [ 236, 8147, 2781, 1858, 1937 ],
    'Dickens, Charles': [ 19337, 1023, 580, 98, 1400 ],
    'Verne, Jules':     [ 103, 12901, 3748, 16457 ]
}

def get_titles(author):
    myTitles = {}
    my_title_list = [] 
    for book_num in myDict[author]:
        title = get_metadata('title', book_num )
        if(title):
            my_title_list.append( list(title)[0] )
        print( my_title_list)
    myTitles[ author ] = my_title_list
    return(myTitles)


def display_options():

    for key in myDict:
        print( key )

    author = input( 'Please copy-and-paste an author from the following list: ')

    titles = get_titles(author)
    print('Titles by:' + author )

    books = titles[ author ]
    for book in books:
        print(book)

    title = input( 'Please copy-and-paste a title from the following list: ')
    print( 'You selected' + title )
    print( 'Building Word Cloud for ' + title )
    

#get_titles()
display_options()


#pprint(myDict['Kipling, Rudyard'])

cache.close()

# print(get_metadata('title', 236))  # prints frozenset([u'Moby Dick; Or, The Whale'])
# print(get_metadata('author', 236)) # prints frozenset([u'Melville, Hermann'])

# print(get_etexts('title', 'The Jungle Book'))  # prints frozenset([2701, ...])
# print(get_etexts('author', 'Kipling, Rudyard'))        # prints frozenset([2701, ...])
# mylist = list(get_etexts('author', 'Kipling, Rudyard'))
# mylist = list(get_etexts('title', 'The Jungle Book'))
# pprint(mylist)
# for i in range(0,len(mylist)):
#     print(get_metadata('author', i))  # prints frozenset([u'Moby Dick; Or, The Whale'])
# # print(list_supported_metadatas()) # prints (u'author', u'formaturi', u'language', ...)
#cache.close()