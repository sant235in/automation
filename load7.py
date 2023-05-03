import time
import random
import requests

# set up the base URL for the CouchDB instance
couchdb_url = 'http://localhost:5984'

# set up the name of the database to use
db_name = 'mydatabase'

# set up the number of documents to insert, update, delete and read
num_docs = 1000

# set up the list of documents to use
docs = []

for i in range(num_docs):
    # generate a random document ID
    doc_id = str(i)

    # generate a random value for the document
    doc_value = random.randint(0, 100)

    # add the document to the list
    docs.append({'_id': doc_id, 'value': doc_value})

# create the database if it doesn't exist
resp = requests.put(f'{couchdb_url}/{db_name}')
if resp.status_code == 201:
    print(f'Created database {db_name}')

# define the function to insert a document into the database
def insert_doc(doc):
    start_time = time.time()
    resp = requests.post(f'{couchdb_url}/{db_name}', json=doc)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Inserted document {doc["_id"]} in {elapsed_time:.6f} seconds')

# define the function to update a document in the database
def update_doc(doc):
    start_time = time.time()
    resp = requests.put(f'{couchdb_url}/{db_name}/{doc["_id"]}', json={'_rev': doc['_rev'], 'value': random.randint(0, 100)})
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Updated document {doc["_id"]} in {elapsed_time:.6f} seconds')

# define the function to delete a document from the database
def delete_doc(doc):
    start_time = time.time()
    resp = requests.delete(f'{couchdb_url}/{db_name}/{doc["_id"]}?rev={doc["_rev"]}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Deleted document {doc["_id"]} in {elapsed_time:.6f} seconds')

# define the function to read a document from the database
def read_doc(doc):
    start_time = time.time()
    resp = requests.get(f'{couchdb_url}/{db_name}/{doc["_id"]}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Read document {doc["_id"]} in {elapsed_time:.6f} seconds')

# perform the CRUD operations simultaneously
for doc in docs:
    insert_doc(doc)
    update_doc(doc)
    delete_doc(doc)
    read_doc(doc)
