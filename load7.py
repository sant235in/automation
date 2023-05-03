import time
import random
import string
import threading
import couchdb

# Set up the database connection
couch = couchdb.Server('http://localhost:5984')
db = couch['mydatabase']

# Define the CRUD functions
def insert_data():
    for i in range(10000):
        doc = {
            'type': 'data',
            'name': ''.join(random.choices(string.ascii_letters, k=10)),
            'value': random.randint(1, 10000)
        }
        db.save(doc)

def update_data():
    for i in range(10000):
        doc_id = random.choice(list(db))
        doc = db[doc_id]
        doc['value'] = random.randint(1, 10000)
        db.save(doc)

def delete_data():
    for i in range(10000):
        doc_id = random.choice(list(db))
        db.delete(db[doc_id])

def read_data():
    for i in range(10000):
        doc_id = random.choice(list(db))
        doc = db[doc_id]

# Define the benchmark function
def benchmark():
    start_time = time.time()

    # Create threads for each CRUD operation
    threads = []
    insert_thread = threading.Thread(target=insert_data)
    update_thread = threading.Thread(target=update_data)
    delete_thread = threading.Thread(target=delete_data)
    read_thread = threading.Thread(target=read_data)
    threads.append(insert_thread)
    threads.append(update_thread)
    threads.append(delete_thread)
    threads.append(read_thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for the threads to finish
    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

# Run the benchmark function
benchmark()
