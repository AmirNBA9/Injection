from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['dataset']
collection = db['imp']

# Find all documents with duplicate values
pipeline = [
    {'$group': {
        '_id': {
            'field1': '$field1',
            'field2': '$field2'
        },
        'count': {'$sum': 1},
        'docs': {'$push': {'_id': '$_id', 'createdAt': '$createdAt'}}
    }},
    {'$match': {
        'count': {'$gt': 1}
    }}
]

# Remove the duplicate documents, keeping the newest one
for doc in collection.aggregate(pipeline):
    documents_to_keep = sorted(doc['docs'], key=lambda x: x['createdAt'], reverse=True)[0]['_id']
    documents_to_remove = [d['_id'] for d in doc['docs'][1:]]
    for doc_id in documents_to_remove:
        collection.delete_one({'_id': doc_id})
        print(f"Deleted document with ID: {doc_id}")

print("Duplicate documents removal completed!")
