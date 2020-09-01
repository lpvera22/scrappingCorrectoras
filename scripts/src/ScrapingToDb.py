import sys
# print(sys.path)
from pymongo import MongoClient,DESCENDING, ASCENDING
sys.path.append('database/')
from db import MongoAPI
import pandas as pd


data = {
    "database": "DEVCorretoras",
    "collection": "",
}


def registerUrls():
    data["collection"] = 'urls'
    dfURLS= pd.read_csv('scripts/out/urlsToDB.csv')
    dfURLS['state']='todo'
    
    dfURLS.reset_index(inplace=True)
    
    dfURLS=dfURLS.fillna(-1)
    print(dfURLS)
    data_dict = dfURLS.to_dict('records')
    mongo_obj = MongoAPI(data)
    # mongo_obj.collection.create_index([("url", DESCENDING), ("cep", ASCENDING)], unique=True)
    try:
        mongo_obj.writeMany(data_dict)
    except:
        print('Already all inserted....in DB')
        pass
    
def registerImages():
    data["collection"] = 'imgs'
    dfIMGS= pd.read_csv('scripts/out/imgstoDB.csv')
    dfIMGS.reset_index(inplace=True)
    
    dfIMGS=dfIMGS.fillna(-1)
    
    data_dict = dfIMGS.to_dict('records')
    print(dfIMGS)
    
    mongo_obj = MongoAPI(data)
    
    mongo_obj.writeMany(data_dict)
    
def getScrapingtoDb():
    print('TO DB....')
    registerUrls()
    registerImages()
