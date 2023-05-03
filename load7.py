import time
import random
import string
import couchdb

# Set up connection to CouchDB
couch = couchdb.Server('http://localhost:5984/')
db_name = 'test_db'
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# Define functions for CRUD operations
def create_document():
    doc_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    doc_data = {'random_data': ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))}
    db.save(doc_data)
    return doc_id

def read_document(doc_id):
    doc = db.get(doc_id)
    return doc['_rev']

def update_document(doc_id, doc_rev):
    doc = db.get(doc_id)
    doc['random_data'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
    db.save(doc)

def delete_document(doc_id, doc_rev):
    doc = db.get(doc_id)
    db.delete(doc)

# Define function to capture performance benchmark of CRUD operations
def measure_performance():
    create_times = []
    read_times = []
    update_times = []
    delete_times = []

    for i in range(1000):
        # Measure time for create operation
        start_time = time.time()
        doc_id = create_document()
        create_times.append(time.time() - start_time)

        # Measure time for read operation
        start_time = time.time()
        doc_rev = read_document(doc_id)
        read_times.append(time.time() - start_time)

        # Measure time for update operation
        start_time = time.time()
        update_document(doc_id, doc_rev)
        update_times.append(time.time() - start_time)

        # Measure time for delete operation
        start_time = time.time()
        delete_document(doc_id, doc_rev)
        delete_times.append(time.time() - start_time)

    # Print performance benchmark results
    print(f'Average create time: {sum(create_times)/len(create_times)} seconds')
    print(f'Average read time: {sum(read_times)/len(read_times)} seconds')
    print(f'Average update time: {sum(update_times)/len(update_times)} seconds')
    print(f'Average delete time: {sum(delete_times)/len(delete_times)} seconds')

if __name__ == '__main__':
    measure_performance()
