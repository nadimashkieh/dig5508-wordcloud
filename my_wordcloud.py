
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.acquire import get_metadata_cache
from gutenberg.query import list_supported_metadatas
from pprint import pprint
from collections import defaultdict 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 

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

#myDict = {
#     'Kipling, Rudyard': [ 236, 8147, 2781, 1858, 1937 ],
#     'Dickens, Charles': [ 19337, 1023, 580, 98, 1400 ],
#     'Verne, Jules':     [ 103, 12901, 3748, 16457 ]
# }

def get_all_titles():
    my_catalog = {}

    for i in range(1, 65000):
        my_title_list = [] 
        title = get_metadata('title', i )
        if(title):
            lang = list( get_metadata('language', i ))[0]
            if ( lang == 'en' ):
                my_title_list.append( list( get_metadata('author', i )))
                my_title_list.append( i )
                my_catalog[ list(title)[0] ] = my_title_list
    return(my_catalog)

# def get_titles(author):
#     myTitles = {}
#     my_title_list = [] 
#     for book_num in myDict[author]:
#         title = get_metadata('title', book_num )
#         if(title):
#             my_title_list.append( list(title)[0] )
#         print( my_title_list)
#     myTitles[ author ] = my_title_list
#     return(myTitles)


def display_options(catalog):

    search_term = input( 'Please enter a search term for an author for a title: ')

    for key in catalog:
        if key.find( search_term ) != -1 :
            print( str( catalog[ key ][1]) + ') ' + key )
    
    title = input( 'Please copy-and-paste a title numberfrom the above list: ')
    print( 'You selected: ' + title )
    text = strip_headers(load_etext( int(title) )).strip()
    print(text)

# def display(text):
#     df=[]
#     df = pd.read_html(text)

#     comment_words = '' 
#     stopwords = set(STOPWORDS) 
    
#     #print( 'Building Word Cloud for ' + text )
#     for val in df.CONTENT: 

#         # typecaste each val to string 
#         val = str(val) 
    
#         # split the value 
#         tokens = val.split() 
        
#         # Converts each token into lowercase 
#         for i in range(len(tokens)): 
#             tokens[i] = tokens[i].lower() 
        
#         comment_words += " ".join(tokens)+" "
    
#     wordcloud = WordCloud(width = 800, height = 800, 
#                     background_color ='white', 
#                     stopwords = stopwords, 
#                     min_font_size = 10).generate(comment_words) 
    
#     # plot the WordCloud image                        
#     plt.figure(figsize = (8, 8), facecolor = None) 
#     plt.imshow(wordcloud) 
#     plt.axis("off") 
#     plt.tight_layout(pad = 0) 
    
#     plt.show()

catalog = get_all_titles()
display_options( catalog )


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
#print(list_supported_metadatas()) # prints (u'author', u'formaturi', u'language', ...)
#cache.close()