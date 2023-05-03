import time
import random
import string
import requests

COUCHDB_URL = "http://localhost:5984"
DB_NAME = "test_db"
NUM_OPERATIONS = 1000

# Generate random data
def generate_data():
    data = {
        "name": "".join(random.choices(string.ascii_letters, k=10)),
        "age": random.randint(1, 100),
        "address": "".join(random.choices(string.ascii_letters + string.digits, k=20))
    }
    return data

# Measure the time taken to perform a request
def measure_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    return end_time - start_time

# Insert random data into the database
def insert_data():
    data = generate_data()
    response = requests.post(f"{COUCHDB_URL}/{DB_NAME}", json=data)
    response.raise_for_status()

# Update random data in the database
def update_data():
    response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/_all_docs")
    response.raise_for_status()
    doc_ids = [row["id"] for row in response.json()["rows"]]
    if len(doc_ids) > 0:
        doc_id = random.choice(doc_ids)
        response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/{doc_id}")
        response.raise_for_status()
        data = response.json()
        data["name"] = "".join(random.choices(string.ascii_letters, k=10))
        response = requests.put(f"{COUCHDB_URL}/{DB_NAME}/{doc_id}", json=data)
        response.raise_for_status()

# Delete random data from the database
def delete_data():
    response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/_all_docs")
    response.raise_for_status()
    doc_ids = [row["id"] for row in response.json()["rows"]]
    if len(doc_ids) > 0:
        doc_id = random.choice(doc_ids)
        response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/{doc_id}")
        response.raise_for_status()
        data = response.json()
        response = requests.delete(f"{COUCHDB_URL}/{DB_NAME}/{doc_id}?rev={data['_rev']}")
        response.raise_for_status()

# Read random data from the database
def read_data():
    response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/_all_docs")
    response.raise_for_status()
    doc_ids = [row["id"] for row in response.json()["rows"]]
    if len(doc_ids) > 0:
        doc_id = random.choice(doc_ids)
        response = requests.get(f"{COUCHDB_URL}/{DB_NAME}/{doc_id}")
        response.raise_for_status()

# Measure the performance of each operation
insert_times = []
update_times = []
delete_times = []
read_times = []
for i in range(NUM_OPERATIONS):
    insert_times.append(measure_time(insert_data))
    update_times.append(measure_time(update_data))
    delete_times.append(measure_time(delete_data))
    read_times.append(measure_time(read_data))

# Output the results
print("Insert times (s):")
print(f"    min: {min(insert_times)}")
print(f"    max: {max(insert_times)}")
print(f"    avg: {sum(insert_times) / len(insert_times)}")
print("Update times (s):")
print(f"    min: {min(update_times)}")
print(f"    max: {max(update_times)}")
print(f
