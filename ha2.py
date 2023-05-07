import couchdb
import random
import string
import time

# Set up CouchDB server and database
server = couchdb.Server('http://localhost:5984/')
db_name = 'test_db'
if db_name not in server:
    db = server.create(db_name)
else:
    db = server[db_name]

# Define the number of documents to generate
num_docs = 1000

# Define the size of each document
doc_size = 1024

# Define the write acknowledgment level
acknowledgment = 'majority'

# Generate and insert random documents
for i in range(num_docs):
    # Generate random data for document
    data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=doc_size))

    # Create document ID
    doc_id = f"doc_{i}"

    # Insert document into database with write acknowledgment
    doc = {'data': data}
    db[doc_id] = doc
    res = db[doc_id].revs_info()

    # Wait for write acknowledgment
    while len(res) < 2:
        time.sleep(0.1)
        res = db[doc_id].revs_info()
