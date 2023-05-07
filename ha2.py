import requests
import json
import time

# Configurations
base_url = "http://<haproxy-node>:<port>"
db_name = "test_db"
username = "<couchdb-username>"
password = "<couchdb-password>"
doc_size = 1024  # in bytes
num_docs = 1000
num_iterations = 10

# Generate random data with index on a field
docs = []
for i in range(num_docs):
    doc = {"index": i}
    doc["data"] = "a" * doc_size
    docs.append(doc)

# Set up authentication header
auth_header = requests.auth.HTTPBasicAuth(username, password)

# Create database if it does not exist
db_url = f"{base_url}/{db_name}"
db_exists = requests.head(db_url, auth=auth_header)
if db_exists.status_code == 404:
    requests.put(db_url, auth=auth_header)

# Start benchmarking
total_time = 0
for i in range(num_iterations):
    print(f"Iteration {i+1}")
    start_time = time.time()

    # Insert documents
    for doc in docs:
        url = f"{db_url}/{doc['index']}"
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=json.dumps(doc), headers=headers, auth=auth_header, params={"w": 2})
        assert response.ok

    # Read documents
    for doc in docs:
        url = f"{db_url}/{doc['index']}"
        response = requests.get(url, auth=auth_header, params={"r": 2})
        assert response.ok

    # Update documents
    for doc in docs:
        url = f"{db_url}/{doc['index']}"
        doc["data"] = "b" * doc_size
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=json.dumps(doc), headers=headers, auth=auth_header, params={"w": 2})
        assert response.ok

    # Delete documents
    for doc in docs:
        url = f"{db_url}/{doc['index']}"
        response = requests.delete(url, auth=auth_header, params={"w": 2})
        assert response.ok

    end_time = time.time()
    iteration_time = end_time - start_time
    total_time += iteration_time
    print(f"Iteration time: {iteration_time:.2f}s")

# Calculate average time per iteration
avg_time = total_time / num_iterations
print(f"Average time per iteration: {avg_time:.2f}s")
