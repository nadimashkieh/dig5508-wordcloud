# Start with loading all necessary libraries
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.acquire import get_metadata_cache
from gutenberg.query import list_supported_metadatas
from pprint import pprint
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# create a book object
class book:
    def __init__(self, index, author, title, subject ):
        self.index = index
        self.author = author
        self.title = title
        self.subject = subject
    
    def get_book_author( self ):
        return self.author

    def get_book_title( self ):
        return self.title
    
    def get_book_index(self):
        return self.index

    def get_book_subject(self):
        return self.subject

# create a catalog object
class book_catalog:
    def __init__( self ):
        self.books = []

    def get_books( self ):
        return self.books

    def add_book( self, book ):
        self.books.append( book )

    def get_book( self, index ):
        for book in self.books:
            if int(book.index) == int(index):
                return book
        return( None )

    def get_authors( self ):
        authors = []
        for book in self.books:
            if book.author not in authors:
                authors.append( book.author )
        authors.sort()
        for author in authors:
            print( author )

    def get_titles( self ):
        titles = []
        for book in self.books:
            if book.title not in titles:
                titles.append( book.title )
        return titles.sort()      

    def get_subjects( self ):
        subjects = []
        for book in self.books:
            if book.subject not in subjects:
                subjects.append( book.subject )
        return subjects.sort()

    def display_titles_by_author( self ):
        authors = {}
        for book in self.books:
            authors[ book.author ] = str( book.index ) + ') ' + '[ ' + book.title + ' ]'

        for author in authors:
            print( f"{'[ ' + author + ' ]':>50}" + ' ==> ' + authors[ author ] )
        return

# Get books from the metadata
def get_all_titles():
    my_catalog = book_catalog()

    for i in range(1, 65000):

        title = ''.join( list( get_metadata( 'title', i ) ) )

        if( title ):
            lang = list( get_metadata('language', i ))[0]
            if lang == 'en':   
                my_book = book( 
                        i, 
                        ''.join( list( get_metadata( 'author', i ) ) ).replace("\n", " ").replace("\r", " "), 
                        ''.join( list( get_metadata( 'title', i ) ) ).replace("\n", " ").replace("\r", " "),
                        ''.join( list( get_metadata( 'subject', i ) ) ).replace("\n", " ").replace("\r", " ") 
                        )  
                my_catalog.add_book( my_book )
    return( my_catalog )

# wordcloud
def display_word_cloud( text ):

    comment_words = '' 
    stopwords = set(STOPWORDS) 
    
    tokens = text.split() 

    # Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
       # my_word_frequency[ tokens[i] ] += 1

    comment_words += " ".join(tokens)+" "
   
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

# Search options for user
def search_display_options( my_catalog ):
    search_result_catalog = book_catalog()

    search_type = input('Please select a search type: Author, Subject, Title [Aa/Ss/Tt]:  ')

    if  search_type == 'A' or search_type == 'a':
        search_term = input( 'Please enter a search term for an Author: ')
    elif search_type == 'T' or search_type == 't' :
        search_term = input( 'Please enter a search term for a Title: ')
    elif search_type == 'S' or search_type == 's':
        search_term = input( 'Please enter a search term for a Subject: ')
    else:
        print( 'Invalid search type...')
        return

    # set match flag to false
    match = False
    # fill up a set of all the titles that match the search
    for my_book in my_catalog.get_books():
        if ( search_type == 'a' or search_type == 'A' )  and set( my_book.get_book_author().lower().split(' ') ).intersection( set( search_term.lower().split( ' ' ) ) ) :
            search_result_catalog.add_book( my_book )
            match = True

        if ( search_type == 't' or search_type == 'T' )  and set( my_book.get_book_title().lower().split(' ')  ).intersection( set( search_term.lower().split( ' ' ) ) ) :
            search_result_catalog.add_book( my_book )
            match = True

        if ( search_type == 's' or search_type == 'S' )  and set( my_book.get_book_subject().lower().split(' ')  ).intersection( set( search_term.lower().split( ' ' ) ) ) :
            search_result_catalog.add_book( my_book )
            match = True

    
    search_result_catalog.display_titles_by_author()
    
    if match:
        title_num = input( 'Please type a title number from the above list: ')
   
        print( 'Displaying Word Cloud in [Subject: ' + my_book.get_book_subject() + '] for [Title: ' + my_book.get_book_title() + '] by [Author:' + my_book.get_book_author() + ']'  )
        try:
            my_book = search_result_catalog.get_book( title_num )
            return( strip_headers( load_etext( int( title_num ) ) ).strip() )  # call that gets bok text from gutenberg
        except:
            print ('Failed to find a textual download candidate for ' + my_book.get_book_title() )
            return(None)
    else:
        print('No matches found for [' + search_term + ']...')
        return(None)
    


##
## main
##
cache = get_metadata_cache()
#cache.populate()
cache.open()
graph = cache.graph
my_catalog = get_all_titles()

more_titles = 'y'
while more_titles == 'y' or more_titles == 'Y':
    book_text = search_display_options( my_catalog )
    if book_text:
        display_word_cloud( book_text )
    more_titles = input('Would you like to search again: [y/n]')


cache.close()

