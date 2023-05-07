import random
import string
import time
import couchdb

# Set up the CouchDB client and database
server = couchdb.Server("http://localhost:5984/")
db = server['my_database']

# Generate random documents with a document size of 1KB
def generate_random_doc():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=1024))
    return {'data': random_string}

# Write the generated documents to the database with acknowledgment w=2
def write_docs():
    doc_list = [generate_random_doc() for i in range(1000)]
    result = db.update(doc_list, w=2)
    return result

# Run the write_docs function in a loop to simulate high workload on the cluster
start_time = time.time()
for i in range(10):
    write_docs()
end_time = time.time()

# Print the time taken to write the documents
print("Time taken to write 10,000 documents with acknowledgment w=2:", end_time - start_time, "seconds")
