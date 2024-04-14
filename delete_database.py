from pymongo.mongo_client import MongoClient
import os

mongo_password = os.environ['MONGO_PASSWORD']


def delete_database(database_url, database_name, collection_name):
  client = MongoClient(database_url)
  try:
    database = client[database_name]
    if collection_name in database.list_collection_names():
      database[collection_name].drop()
      print(f"Collection {collection_name} deleted successfully")
    else:
      print(
          f"Collection {collection_name} NOT FOUND in the database {database_name}"
      )
  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  mongo_uri = f"mongodb+srv://TrialH23:{mongo_password}@cluster0.a48kdir.mongodb.net/?retryWrites=true&w=majority"
  database_name = "github_issues"
  collection_name = "issues"
  delete_database(mongo_uri, database_name, collection_name)
