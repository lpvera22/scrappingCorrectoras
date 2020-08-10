from database.db import MongoAPI
import pandas as pd

data = {
    "database": "Corretoras",
    "collection": "",
}


def getScrapingtoDb():
    data["collection"] = 'urls'
    df = pd.read_csv('scripts/out/urlFinal.csv')
    df['state'] = 'todo'
    df.reset_index(inplace=True)
    data_dict = df.to_dict('records')
    mongo_obj = MongoAPI(data)
    mongo_obj.writeMany(data_dict)


if __name__ == '__main__':
    getScrapingtoDb()
