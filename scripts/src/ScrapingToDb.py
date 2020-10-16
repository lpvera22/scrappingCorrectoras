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
    data_dict = dfURLS.to_dict('records')
    to_register=dict(zip(dfURLS['url'].unique(), [[] for i in dfURLS['url'].unique()]))
    
    for u in data_dict:
        url=u['url']
        c=u['cep']
        listceps=to_register[url]
        if c not in listceps:
            listceps.append(c)
            to_register[url]=listceps

     
    
    
    dfURLS=dfURLS.fillna(-1)
    
    mydb = MongoAPI(data)
    output=mydb.read()
    
    
    
    #checking the urls already in the db
    dbUrls={}
    for i in output:
        dbUrls[i['url']]=i['ceps']
    
    
    for key in to_register:
        if key not in dbUrls:
            data['Document']={
                'url':key,
                'ceps':to_register[key],
                'state':'todo', 
                'domain':key[key[8:].find('/') + 8:].replace('/', '')

            }
            mydb.write(data)
        else:
            for i in to_register[key]:
                if i not in dbUrls[key]:
                    dbUrls[key].append(i)
            data['Filter']={'url':key}
            data['ceps']={'ceps':dbUrls[key]}
            data['state']='todo'

            response = mydb.updateUrl()
            


    

    


    
    
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
    # registerUrls()
    registerImages()
