from pymongo import MongoClient


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient(
            'mongodb+srv://admin:admin123@cluster0.hzfwu.mongodb.net/test?authSource=admin&replicaSet=atlas-nb4s9h-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true ')

        database = data['database']
        collection = data['collection']

        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find({})

        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        print(output)
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
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
