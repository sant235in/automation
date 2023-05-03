import random
import string
import time
import threading
import uuid
from couchdb import Server

NUM_THREADS = 10
NUM_DOCS = 1000
DB_NAME = 'mydb'
DB_URL = 'http://localhost:5984/'

def random_string(length):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_doc():
    """Generate a random document."""
    doc_id = str(uuid.uuid4())
    doc = {'_id': doc_id, 'name': random_string(10), 'age': random.randint(20, 50)}
    return doc

def insert_docs():
    """Insert documents into CouchDB."""
    server = Server(DB_URL)
    db = server[DB_NAME]
    for i in range(NUM_DOCS):
        doc = generate_doc()
        db.save(doc)

def update_docs():
    """Update documents in CouchDB."""
    server = Server(DB_URL)
    db = server[DB_NAME]
    for i in range(NUM_DOCS):
        doc_id = str(i+1)
        doc = db.get(doc_id)
        doc['name'] = random_string(10)
        db.save(doc)

def delete_docs():
    """Delete documents from CouchDB."""
    server = Server(DB_URL)
    db = server[DB_NAME]
    for i in range(NUM_DOCS):
        doc_id = str(i+1)
        doc = db.get(doc_id)
        db.delete(doc)

def read_docs():
    """Read documents from CouchDB."""
    server = Server(DB_URL)
    db = server[DB_NAME]
    for i in range(NUM_DOCS):
        doc_id = str(i+1)
        doc = db.get(doc_id)

# Start the timer
start_time = time.time()

# Start the threads for CRUD operations
threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target=insert_docs)
    threads.append(thread)
    thread.start()

for i in range(NUM_THREADS):
    thread = threading.Thread(target=update_docs)
    threads.append(thread)
    thread.start()

for i in range(NUM_THREADS):
    thread = threading.Thread(target=delete_docs)
    threads.append(thread)
    thread.start()

for i in range(NUM_THREADS):
    thread = threading.Thread(target=read_docs)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# End the timer
end_time = time.time()

# Print the benchmarking results
print(f'Total time taken: {end_time - start_time:.2f} seconds')
print(f'Average time per operation: {(end_time - start_time) / (NUM_THREADS * NUM_DOCS * 4):.6f} seconds')
