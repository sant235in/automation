import time
import random
import couchdb

# Define CouchDB connection parameters
couch_url = 'http://localhost:5984/'
db_name = 'mydatabase'
couch = couchdb.Server(couch_url)

# Create database if it doesn't exist
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# Define number of documents to insert, update, delete and read
num_docs = 10000

# Define sample document structure
doc_template = {
    'type': 'mydoc',
    'name': '',
    'age': 0,
    'email': '',
    'address': '',
}

# Insert documents into database
start_time = time.time()
for i in range(num_docs):
    doc = doc_template.copy()
    doc['name'] = f'name_{i}'
    doc['age'] = random.randint(18, 65)
    doc['email'] = f'name_{i}@example.com'
    doc['address'] = f'Address {i}'
    db.save(doc)
insert_time = time.time() - start_time

# Update documents in database
start_time = time.time()
for i in range(num_docs):
    doc = db.get(f'mydoc_{i}')
    doc['age'] = random.randint(18, 65)
    db.save(doc)
update_time = time.time() - start_time

# Delete documents from database
start_time = time.time()
for i in range(num_docs):
    doc = db.get(f'mydoc_{i}')
    db.delete(doc)
delete_time = time.time() - start_time

# Read documents from database
start_time = time.time()
for i in range(num_docs):
    doc = db.get(f'mydoc_{i}')
read_time = time.time() - start_time

# Print results
print(f'Insert time: {insert_time}')
print(f'Update time: {update_time}')
print(f'Delete time: {delete_time}')
print(f'Read time: {read_time}')
