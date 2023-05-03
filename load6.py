import random
import string
import time
import concurrent.futures
import requests


# Function to generate random document ID
def random_doc_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


# Function to generate random document content
def random_doc_content():
    return {
        'title': ''.join(random.choices(string.ascii_lowercase, k=10)),
        'body': ''.join(random.choices(string.ascii_lowercase, k=50))
    }


# Function to insert a document
def insert_doc():
    url = 'http://localhost:5984/mydatabase'
    headers = {'Content-Type': 'application/json'}
    data = {'_id': random_doc_id(), 'content': random_doc_content()}
    response = requests.post(url, headers=headers, json=data)
    return response


# Function to update a document
def update_doc():
    url = 'http://localhost:5984/mydatabase/' + random_doc_id()
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    if response.status_code == 200:
        doc = response.json()
        doc['content'] = random_doc_content()
        response = requests.put(url, headers=headers, json=doc)
    return response


# Function to delete a document
def delete_doc():
    url = 'http://localhost:5984/mydatabase/' + random_doc_id()
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    if response.status_code == 200:
        doc = response.json()
        doc['_deleted'] = True
        response = requests.put(url, headers=headers, json=doc)
    return response


# Function to read a document
def read_doc():
    url = 'http://localhost:5984/mydatabase/' + random_doc_id()
    response = requests.get(url)
    return response


# Main function to run the benchmark
def run_benchmark(num_ops):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        insert_futures = []
        update_futures = []
        delete_futures = []
        read_futures = []
        start_time = time.time()
        for i in range(num_ops):
            insert_futures.append(executor.submit(insert_doc))
            update_futures.append(executor.submit(update_doc))
            delete_futures.append(executor.submit(delete_doc))
            read_futures.append(executor.submit(read_doc))
        for future in concurrent.futures.as_completed(insert_futures + update_futures + delete_futures + read_futures):
            if future.exception() is not None:
                print(future.exception())
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Total time taken for {num_ops} operations: {total_time:.2f} seconds')
    print(f'Throughput: {num_ops / total_time:.2f} operations per second')


if __name__ == '__main__':
    run_benchmark(1000)  # Change the number of operations as required
