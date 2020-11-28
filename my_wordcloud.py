# Start with loading all necessary libraries
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.acquire import get_metadata_cache
from gutenberg.query import list_supported_metadatas
from pprint import pprint
import json
from collections import defaultdict 
import matplotlib.pyplot as plt 
import pandas as pd 
from pandas.io.json import json_normalize
import numpy as np
#import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
#% matplotlib inline

#c:\intelpython3\lib\site-packages\matplotlib\__init__.py:
import warnings
warnings.filterwarnings("ignore")


cache = get_metadata_cache()
#cache.populate()


cache.open()
graph = cache.graph


def get_all_titles():
    my_catalog = {}

    for i in range(1, 65000):
        my_title_list = [] 
        title = get_metadata('title', i )
        if(title):
            lang = list( get_metadata('language', i ))[0]
            if lang == 'en':
                my_title_list.append( list( get_metadata('author', i )))
                my_title_list.append( i )
                my_catalog[ list(title)[0] ] = my_title_list
    return(my_catalog)




def display(text):

    #df = pd.DataFrame(book,columns=['title','author', 'number', 'text'])
   
    comment_words = '' 
    stopwords = set(STOPWORDS) 
    
    tokens = text.split() 

   # my_word_frequency = {}

    # Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
       # my_word_frequency[ tokens[i] ] += 1

    comment_words += " ".join(tokens)+" "
    #pprint( my_word_frequency)


    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 
    
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    
    plt.show()



def display_options(catalog):

    search_term = input( 'Please enter a search term for an author or a title: ')

    match = False

    for key in catalog:
        #if key.find( search_term ) != -1 :
        if set( key.split(' ') ).intersection( set(search_term.split(' ') ) ):
            print( str( catalog[ key ][1]) + ') ' + key )
            match = True
    
    if match:
        title_num = input( 'Please type a title number from the above list: ')
        title_text = list(get_metadata('title', title_num ))[0]
        print( 'You selected: ' + title_text )
        try:
            return( strip_headers(load_etext( int(title_num) )).strip() )
        except:
            print ('Failed to find a textual download candidate for ' + title_text )
            return(None)
    else:
        print('No matches found... ')
        return(None)
    
    #display(json.dumps( { "title": title_text, "author": catalog[ title_text ][ 0 ], "number": catalog[ title_text ][ 1 ], "text": text } ))
    #display( json.dumps( [ title_text, catalog[ title_text ][ 0 ], catalog[ title_text ][ 1 ], text ] ) )
    
  


catalog = get_all_titles()
more_titles = 'y'
while more_titles == 'y' or more_titles == 'Y':
    text = display_options( catalog )
    if text:
        display( text )
    more_titles = input('Would you like to search for another title: [y/n]')


cache.close()

