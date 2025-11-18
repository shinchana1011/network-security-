
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://shinchanarai23_db_user:Shinchana2005@cluster0.f5wvucz.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)