from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import sys

def search_review(query, business_name):
   ix = open_dir("indexdir")
   
   with ix.searcher(weighting=scoring.BM25F) as searcher:
      query = QueryParser("review", ix.schema).parse(query)
      results = searcher.search(query, terms=True)
      
      review_results = []
      for hit in results:
         hit_data = dict(hit)
         if hit_data['business_name'] == business_name:
            r = {}
            r['user_name'] = hit_data['username']
            r['date'] = hit_data['date']
            r['review'] = hit_data['review']
            review_results.append(r)
      return review_results      

#search_review("pepperoni pizza",'Little Caesar\'s')