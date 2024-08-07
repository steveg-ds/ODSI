from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidOperation
from bson import ObjectId  # For handling MongoDB ObjectId
from logger_config import logger

class DB:
    """
    A class to handle MongoDB operations for the ODSI project.
    """

    def __init__(self, host='mongodb://localhost', port=27017, db_name='ODSI'):
        """
        Initializes the MongoDB connection.

        Args:
            host (str): MongoDB host URI.
            port (int): MongoDB port number.
            db_name (str): Name of the database to connect to.
        """
        self.client = MongoClient(host)
        self.db = self.client[db_name]
        logger.info("MongoDB connection established.")

    def insert_document(self, collection_name, document):
        """
        Inserts a document into a specified collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to be inserted.

        Returns:
            ObjectId: The ID of the inserted document or None if insertion fails.
        """
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            logger.info(f"Document inserted with id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            return None

    def find_documents(self, collection_name, query={}):
        """
        Finds multiple documents in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.

        Returns:
            list: A list of documents matching the query.
        """
        try:
            collection = self.db[collection_name]
            documents = list(collection.find(query))
            logger.info("Documents found")
            return documents
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []

    def find_one_document(self, collection_name, query={}):
        """
        Finds a single document in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.

        Returns:
            dict: The document matching the query or None if not found.
        """
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            logger.info(f"Document found in {collection_name}: {document['_id']}")
            return document
        except Exception as e:
            logger.error(f"Error finding one document in {collection_name}: {e}")
            return None

    def update_document(self, collection_name, query, update_data):
        """
        Updates a document in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.
            update_data (dict): The data to update in the document.

        Returns:
            int: The number of documents updated.
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {'$set': update_data})
            logger.info(f"Documents updated: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return 0
        
    def add_document_entry(self, collection_name, query, new_field, new_value, update_data={}):
        """
        Adds a new field to a document in a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.
            new_field (str): The field to add.
            new_value: The value of the new field.
            update_data (dict): The data to update in the document.

        Returns:
            int: The number of documents updated.
        """
        try:
            collection = self.db[collection_name]
            
            update_data.setdefault('$set', {})[new_field] = new_value

            result = collection.update_one(query, update_data)
            
            logger.info(f"Documents updated: {result.modified_count}")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return 0

    def delete_document(self, collection_name, query):
        """
        Deletes a document from a specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query to filter documents.

        Returns:
            int: The number of documents deleted.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            logger.info(f"Documents deleted: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return 0

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        try:
            self.client.close()
            logger.info("MongoDB connection closed.")
        except ConnectionFailure as e:
            logger.error(f"Error closing MongoDB connection: {e}")

    def drop_collection(self, collection_name):
        """
        Drops a specified collection from the database.

        Args:
            collection_name (str): The name of the collection.
        """
        try:
            self.db.drop_collection(collection_name)
            logger.info(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            logger.error(f"Error dropping collection: {e}")

    def truncate_collection(self, collection_name):
        """
        Deletes all documents from a specified collection.

        Args:
            collection_name (str): The name of the collection.
        """
        try:
            collection = self.db[collection_name]
            collection.delete_many({})
            logger.info(f"Collection '{collection_name}' truncated successfully.")
        except Exception as e:
            logger.error(f"Error truncating collection: {e}")

    def truncate_all_collections(self):
        """
        Deletes all documents from all collections in the database.
        """
        try:
            for collection_name in self.list_collections():
                self.drop_collection(collection_name)
            logger.info("All collections truncated successfully.")
        except Exception as e:
            logger.error(f"Error truncating collections: {e}")

    def list_collections(self):
        """
        Lists all collections in the database.

        Returns:
            list: A list of collection names.
        """
        try:
            collections = self.db.list_collection_names()
            logger.info(f"Collections listed: {collections}")
            return collections
        except InvalidOperation as e:
            logger.error(f"Error listing collections: {e}")
            return []
