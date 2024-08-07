from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidOperation
from bson import ObjectId  # For handling MongoDB ObjectId
from logger_config import logger

class DB:
    def __init__(self, host='host.docker.internal', port=27017, db_name='ODSI'):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        logger.info("MongoDB connection established.")

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            return None

    def find_documents(self, collection_name, query={}):
        try:
            collection = self.db[collection_name]
            documents = list(collection.find(query))
            return documents
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []

    def find_one_document(self, collection_name, query={}):
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            logger.info(f"Document found: {document['_id']}")
            return document
        except Exception as e:
            logger.error(f"Error finding one document: {e}")
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

    def insert_user(self, username, email, password, firstname, lastname, school):
        try:

            collection = self.db['Users']
            result = collection.insert_one(user_data)
            logger.info(f"User inserted with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting user: {e}")
            return None

    def find_user_by_username(self, username):
        try:
            collection = self.db['Users']
            user = collection.find_one({"username": username})
            logger.info(f"User found: {user}")
            return user
        except Exception as e:
            logger.error(f"Error finding user: {e}")
            return None
# db = DB()

# tournament_name = 'Hot And Spicy Speech and Debate Tournament'
# query = {'tournament_name': tournament_name}
# data = db.find_one_document(collection_name="Tournaments", query=query)
# data