from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

from gutenberg.acquire import get_metadata_cache
from pprint import pprint

#cache = get_metadata_cache()
#cache.populate()

cache = get_metadata_cache()
cache.open()
graph = cache.graph

myDict = {}
for i in range(1,16000):
    author=get_metadata('author', i )
    title=get_metadata('title', i )
    if(author):
        myDict[  list(author)[0]  ] = list(title)[0] 

pprint(myDict)