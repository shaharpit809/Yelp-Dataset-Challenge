import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys
import pandas as pd
 
def createSearchableData(data):   
 
    '''
    Schema definition: title(name of file), path(as ID), content(indexed
    but not stored),textdata (stored text content)
    '''
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        
    schema = Schema(business_id=ID(stored=True), user_id=ID(stored=True), review=TEXT(stored=True), business_name=TEXT(stored=True), date=TEXT(stored=True),username=TEXT(stored=True),review_id=ID(stored=True))
    
    
    ix = create_in("indexdir", schema)
    
    writer = ix.writer()
    for index, r in data.iterrows():
        writer.add_document(business_id=r['business_id'], user_id=r['user_id'], review=r['text'], business_name=r['business_name'], date=r['date'],username=r['username'],review_id=r['review_id'])
    writer.commit()

review_data = pd.read_csv('business_review_users_tags.csv')
data = review_data[['business_id','user_id','text','business_name','date','username','review_id']]
createSearchableData(data)