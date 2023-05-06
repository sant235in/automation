import time
import uuid
import random
import requests

# Configuration
DATABASE_NAME = 'my_database'
SHARD_SERVERS = ['http://localhost:5984', 'http://localhost:5985']
SHARD_COUNT = len(SHARD_SERVERS)
WRITE_CONCERN = 2
READ_CONCERN = 2

# Helper function to generate random data
def generate_data():
    return {
        '_id': str(uuid.uuid4()),
        'name': 'John Doe',
        'age': random.randint(18, 65),
        'email': 'johndoe@example.com',
        'address': {
            'street': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345'
        }
    }

# Helper function to perform CRUD operations on the shard cluster
def perform_operations():
    # Insert
    data = generate_data()
    start_time = time.time()
    response = requests.post(f'{SHARD_SERVERS[0]}/{DATABASE_NAME}/', json=data)
    insert_time = time.time() - start_time
    if response.status_code != 201:
        raise Exception(f'Insert failed with status code {response.status_code}')
    doc_id = response.json()['id']

    # Update
    data['name'] = 'Jane Doe'
    start_time = time.time()
    response = requests.put(f'{SHARD_SERVERS[0]}/{DATABASE_NAME}/{doc_id}', json=data)
    update_time = time.time() - start_time
    if response.status_code != 201:
        raise Exception(f'Update failed with status code {response.status_code}')

    # Read
    start_time = time.time()
    response = requests.get(f'{SHARD_SERVERS[random.randint(0, SHARD_COUNT-1)]}/{DATABASE_NAME}/{doc_id}')
    read_time = time.time() - start_time
    if response.status_code != 200:
        raise Exception(f'Read failed with status code {response.status_code}')

    # Delete
    start_time = time.time()
    response = requests.delete(f'{SHARD_SERVERS[0]}/{DATABASE_NAME}/{doc_id}')
    delete_time = time.time() - start_time
    if response.status_code != 200:
        raise Exception(f'Delete failed with status code {response.status_code}')

    return insert_time, update_time, read_time, delete_time

# Main function to perform the benchmarking
def main():
    # Create database
    for server in SHARD_SERVERS:
        requests.put(f'{server}/{DATABASE_NAME}')

    # Perform operations
    insert_times = []
    update_times = []
    read_times = []
    delete_times = []
    for i in range(1000):
        insert_time, update_time, read_time, delete_time = perform_operations()
        insert_times.append(insert_time)
        update_times.append(update_time)
        read_times.append(read_time)
        delete_times.append(delete_time)

    # Print results
    print(f'Average insert time: {sum(insert_times)/len(insert_times):.3f}s')
    print(f'Average update time: {sum(update_times)/len(update_times):.3f}s')
    print(f'Average read time: {sum(read_times)/len(read_times):.3f}s')
    print(f'Average delete time: {sum(delete_times)/len(delete_times):.3f}s')

if __name__ == '__main__':
    main()
