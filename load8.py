import time
import random
import string
import requests

# Replace with your own database URL and name
DB_URL = 'http://localhost:5984'
DB_NAME = 'test_db'

# Generate a random string of length n
def random_string(n):
    return ''.join(random.choices(string.ascii_letters, k=n))

# Create a new document in the database
def create_document():
    data = {'name': random_string(10), 'age': random.randint(1, 100)}
    response = requests.post(f'{DB_URL}/{DB_NAME}', json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        return None

# Read a document from the database
def read_document(doc_id):
    response = requests.get(f'{DB_URL}/{DB_NAME}/{doc_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Update a document in the database
def update_document(doc_id):
    doc = read_document(doc_id)
    if doc is None:
        return False
    doc['name'] = random_string(10)
    response = requests.put(f'{DB_URL}/{DB_NAME}/{doc_id}', json=doc)
    return response.status_code == 200

# Delete a document from the database
def delete_document(doc_id):
    doc = read_document(doc_id)
    if doc is None:
        return False
    rev = doc['_rev']
    response = requests.delete(f'{DB_URL}/{DB_NAME}/{doc_id}?rev={rev}')
    return response.status_code == 200

# Measure the time taken to perform n iterations of a function
def measure_time(fn, n):
    start_time = time.time()
    for i in range(n):
        fn()
    end_time = time.time()
    return end_time - start_time

# Test the CRUD operations and measure the performance
n = 1000  # Number of iterations
create_time = measure_time(create_document, n)
print(f'Create time per document: {create_time / n:.6f} seconds')

doc_id = create_document()
if doc_id is not None:
    read_time = measure_time(lambda: read_document(doc_id), n)
    print(f'Read time per document: {read_time / n:.6f} seconds')
    update_time = measure_time(lambda: update_document(doc_id), n)
    print(f'Update time per document: {update_time / n:.6f} seconds')
    delete_time = measure_time(lambda: delete_document(doc_id), n)
    print(f'Delete time per document: {delete_time / n:.6f} seconds')
else:
    print('Failed to create a document')
