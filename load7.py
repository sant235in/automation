import time
import random
import string
import requests

COUCHDB_URL = 'http://localhost:5984'
DB_NAME = 'test_db'
NUM_THREADS = 10
NUM_DOCS = 1000

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def insert_document(doc_id):
    doc = {'_id': doc_id, 'name': generate_random_string(10)}
    res = requests.post(f'{COUCHDB_URL}/{DB_NAME}', json=doc)
    return res.status_code == 201

def update_document(doc_id):
    res = requests.get(f'{COUCHDB_URL}/{DB_NAME}/{doc_id}')
    if res.status_code == 200:
        doc = res.json()
        doc['name'] = generate_random_string(10)
        res = requests.put(f'{COUCHDB_URL}/{DB_NAME}/{doc_id}', json=doc)
        return res.status_code == 201
    else:
        return False

def read_document(doc_id):
    res = requests.get(f'{COUCHDB_URL}/{DB_NAME}/{doc_id}')
    return res.status_code == 200

def delete_document(doc_id):
    res = requests.get(f'{COUCHDB_URL}/{DB_NAME}/{doc_id}')
    if res.status_code == 200:
        doc = res.json()
        res = requests.delete(f'{COUCHDB_URL}/{DB_NAME}/{doc_id}?rev={doc["_rev"]}')
        return res.status_code == 200
    else:
        return False

def run_benchmark():
    print('Starting benchmark...')
    insert_times = []
    update_times = []
    read_times = []
    delete_times = []

    doc_ids = [f'doc{i}' for i in range(NUM_DOCS)]

    for i in range(NUM_THREADS):
        insert_times.append([])
        update_times.append([])
        read_times.append([])
        delete_times.append([])

    for doc_id in doc_ids:
        start_time = time.time()

        # Simultaneously perform CRUD operations for each document
        for i in range(NUM_THREADS):
            if insert_document(doc_id):
                insert_times[i].append(time.time() - start_time)
            if update_document(doc_id):
                update_times[i].append(time.time() - start_time)
            if read_document(doc_id):
                read_times[i].append(time.time() - start_time)
            if delete_document(doc_id):
                delete_times[i].append(time.time() - start_time)

    # Print the average time taken for each operation by each thread
    print(f'Insert times: {[sum(insert_times[i])/len(insert_times[i]) for i in range(NUM_THREADS)]}')
    print(f'Update times: {[sum(update_times[i])/len(update_times[i]) for i in range(NUM_THREADS)]}')
    print(f'Read times: {[sum(read_times[i])/len(read_times[i]) for i in range(NUM_THREADS)]}')
    print(f'Delete times: {[sum(delete_times[i])/len(delete_times[i]) for i in range(NUM_THREADS)]}')

if __name__ == '__main__':
    run_benchmark()
