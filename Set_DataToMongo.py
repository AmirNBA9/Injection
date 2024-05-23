import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['dataset']
collection = db['imp']

# Read data from JSON file
with open('finaldataset.json', 'r') as file:
    data = json.load(file)

# Insert data into MongoDB if it doesn't exist
for item in data:
    if collection.count_documents(item) == 0:
        collection.insert_one(item)
    else:
        print(f"Document already exists: {item}")

print('Data insertion completed!')



# Read data from MongoDB
documents = collection.find()

# Print the documents
for document in documents:
    print(document)


