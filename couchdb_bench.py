import time
import random
import couchdb

# Set up CouchDB connection and database
couch = couchdb.Server('http://localhost:5984')
db_name = 'mydb'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Define number of documents to insert and update
num_docs = 1000

# Define number of threads to run simultaneously
num_threads = 10

# Define w and r acknowledgement values
w = 2
r = 2

# Define function to perform CRUD operations
def perform_crud():
    # Insert random documents
    for i in range(num_docs):
        doc = {'data': random.randint(1, 100000)}
        db.save(doc, w=w)

    # Update random documents
    for i in range(num_docs):
        doc_id = random.choice(list(db))
        doc = db[doc_id]
        doc['data'] = random.randint(1, 100000)
        db.save(doc, w=w)

    # Delete random documents
    for i in range(num_docs):
        doc_id = random.choice(list(db))
        doc = db[doc_id]
        db.delete(doc, w=w)

    # Read random documents
    for i in range(num_docs):
        doc_id = random.choice(list(db))
        doc = db.get(doc_id, r=r)

# Define function to run CRUD operations in threads
def run_threads():
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=perform_crud)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Define function to measure performance
def measure_performance():
    start_time = time.time()
    run_threads()
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Total time taken: {total_time:.2f} seconds')
    print(f'Time per operation: {total_time/(num_docs*num_threads*4):.2f} seconds')

# Measure performance
measure_performance()
