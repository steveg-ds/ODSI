from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidOperation
from bson import ObjectId  # For handling MongoDB ObjectId
from logger_config import logger

class DB:
    # def __init__(self, host='mongodb://mongo-db:27017/', db_name='ODSI'):
    def __init__(self, host='127.0.0.1', port=27017, db_name='ODSI'):
        self.client = MongoClient(host)
        self.db = self.client[db_name]
        logger.info("MongoDB connection established.")

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Document inserted with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            return None

    def find_documents(self, collection_name, query={}):
        try:
            collection = self.db[collection_name]
            documents = list(collection.find(query))
            logger.info(f"Documents found")
            return documents
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []

    def find_one_document(self, collection_name, query={}):
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            logger.info(f"Document found in {collection_name}: {document['_id']}")
            return document
        except Exception as e:
            logger.error(f"Error finding one document in {collection_name}: {e}")
            return None

    def update_document(self, collection_name, query, update_data):
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': update_data})
            logger.info(f"Documents updated: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return 0
        
    def add_document_entry(self, collection_name, query,  new_field, new_value, update_data={}):
        try:
            collection = self.db[collection_name]
            
            # Include the new field and its value in the update_data dictionary
            update_data.setdefault('$set', {})[new_field] = new_value

            result = collection.update_one(query, update_data)
            
            logger.info(f"Documents updated: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return 0

    def delete_document(self, collection_name, query):
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            logger.info(f"Documents deleted: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return 0

    def close_connection(self):
        try:
            self.client.close()
            logger.info("MongoDB connection closed.")
        except ConnectionFailure as e:
            logger.error(f"Error closing MongoDB connection: {e}")

    def drop_collection(self, collection_name):
        try:
            self.db.drop_collection(collection_name)
            logger.info(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            logger.error(f"Error dropping collection: {e}")

    def truncate_collection(self, collection_name):
        try:
            collection = self.db[collection_name]
            collection.delete_many({})
            logger.info(f"Collection '{collection_name}' truncated successfully.")
        except Exception as e:
            logger.error(f"Error truncating collection: {e}")

    def truncate_all_collections(self):
        try:
            for collection_name in self.list_collections():
                self.drop_collection(collection_name)
            logger.info("All collections truncated successfully.")
        except Exception as e:
            logger.error(f"Error truncating collections: {e}")

    def list_collections(self):
        try:
            collections = self.db.list_collection_names()
            logger.info(f"Collections listed: {collections}")
            return collections
        except InvalidOperation as e:
            logger.error(f"Error listing collections: {e}")
            return []


