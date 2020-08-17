import sys
# sys.path.append('database/')
from db import MongoAPI
# from database.db import MongoAPI
import pandas as pd


data = {
    "database": "Corretoras",
    "collection": "",
}


def getScrapingtoDb():
    data["collection"] = 'urls'
    df = pd.read_csv('scripts/out/urlFinal.csv')
    dfImgUrl = pd.read_csv('scripts/out/imgUrls.csv',sep=';')
    dfImgUrl['domain']=dfImgUrl['url'].apply(lambda x: x[x[8:].find('/') + 8:].replace('/', ''))
    dfImgUrl=dfImgUrl[dfImgUrl['domain'].isin(df['domain'].to_list())]
    
    
    
    dfFeat=df[['domain','font','url','SSL','title','keywords','malicious','date']]
    
    dfFeat['state'] = 'todo'
    dfFeat.reset_index(inplace=True)
    
    dfFeat=dfFeat.fillna(-1)
    data_dict = dfFeat.to_dict('records')
    mongo_obj = MongoAPI(data)
    mongo_obj.writeMany(data_dict)
    
    dfColor=df[['domain','0','1','2','3','4','5','6','7','8','9']]
    data['collection']='colors'
    
    dfColor.reset_index(inplace=True)
    
    dfColor=dfColor.fillna(-1)
    data_dict = dfColor.to_dict('records')
    mongo_obj = MongoAPI(data)
    mongo_obj.writeMany(data_dict)
    
    data['collection']='images'
    
    dfImgUrl.reset_index(inplace=True)
    
    dfImgUrl=dfImgUrl.fillna(-1)
    data_dict = dfImgUrl.to_dict('records')
    mongo_obj = MongoAPI(data)
    mongo_obj.writeMany(data_dict)
    
    
    


