from pymongo import MongoClient,DESCENDING, ASCENDING


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient(
            'mongodb+srv://admin:admin123@cluster0.hzfwu.mongodb.net/test?authSource=admin&replicaSet=atlas-nb4s9h-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true ')

        database = data['database']
        collection = data['collection']

        cursor = self.client[database]
        self.collection = cursor[collection]
        # if collection=='urls':
        #     self.collection.create_index([("url", DESCENDING), ("cep", ASCENDING)], unique=True)
        self.data = data

    def read(self):
        documents = self.collection.find({})

        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        
        return output
    def readQuery(self,q):
        print(q)
        documents = self.collection.find(q)

        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        
        return output
        
    
    def readFromUrl(self):
        documents = self.collection.find({"url":self.data['url']})

        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        
        return output

    def write(self, data):
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def writeMany(self, dataDF):
        response = self.collection.insert_many(dataDF)
        output = {'Status': 'Successfully Inserted'}
        return output

    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['state']}
        
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
    def deleteAll(self):
        response=self.collection.delete_many({})
        output = {'Status': 'Collection Successfully Deleted' }
        return output
        
