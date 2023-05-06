import time
import random
import string
import requests

# Set the parameters for the performance test
num_docs = 1000
num_threads = 10
base_url = "http://localhost:5984/db"
auth = ("admin", "password")
headers = {"Content-Type": "application/json"}
params = {"w": "2", "r": "2"}

# Define a function to generate random documents
def generate_doc():
    doc = {}
    doc["_id"] = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    doc["name"] = "".join(random.choices(string.ascii_lowercase, k=10))
    doc["age"] = random.randint(18, 80)
    return doc

# Define a function to perform CRUD operations on the database
def crud_ops():
    # Generate a random document
    doc = generate_doc()
    # Insert the document
    resp = requests.post(base_url, auth=auth, headers=headers, json=doc, params=params)
    doc["_rev"] = resp.json()["rev"]
    # Update the document
    doc["age"] = random.randint(18, 80)
    resp = requests.put(base_url + "/" + doc["_id"], auth=auth, headers=headers, json=doc, params=params)
    doc["_rev"] = resp.json()["rev"]
    # Delete the document
    resp = requests.delete(base_url + "/" + doc["_id"] + "?rev=" + doc["_rev"], auth=auth, params=params)
    # Read the document
    resp = requests.get(base_url + "/" + doc["_id"], auth=auth, headers=headers, params=params)

# Define a function to measure the performance of the CRUD operations
def measure_perf():
    start_time = time.time()
    # Start multiple threads to perform CRUD operations simultaneously
    for i in range(num_threads):
        for j in range(int(num_docs/num_threads)):
            crud_ops()
    end_time = time.time()
    total_time = end_time - start_time
    print("Total time taken: %.2f seconds" % total_time)
    print("Throughput: %.2f requests/second" % (num_docs*num_threads/total_time))

# Call the measure_perf function to measure the performance
measure_perf()
