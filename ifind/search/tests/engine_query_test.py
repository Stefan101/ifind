
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
#from ifind.search.cache import *

#query = Query('dog', top=10)
query = Query('glasgow', top=50)
query2 = Query('glasgow', top=10)
#query = Query('awful bus glasgow', source_type="Web", format='JSON', top=10, skip=0)
#query2 = Query('milk death', result_type="web", format='JSON', top=70, skip=0)
#query2 = Query("furnace", result_type='recent', top=5)

#raise SearchException(__file__.split('/')[-1].split('.')[0], "PROBLEM")

engine = EngineFactory("wikipedia")
engine2 = EngineFactory("wikipedia")

#response = engine.search(query)

query2.top=50

print query == query2