import random
import string
import time
import couchdb

# Connect to CouchDB shard cluster
nodes = ['http://node1:5984', 'http://node2:5984', 'http://node3:5984']
couch = couchdb.Cluster(nodes)

# Create database and enable sharding
db_name = 'mydb'
db = couch.create(db_name, partitioned=True)

# Create index on a field
db.create_index(['field'])

# Generate random data with 1KB document size and index on a field
doc_size = 1024  # bytes
doc_count = 10000
docs = []
for i in range(doc_count):
    doc = {}
    doc['field'] = ''.join(random.choices(string.ascii_lowercase, k=10))
    doc['data'] = ''.join(random.choices(string.ascii_lowercase, k=doc_size))
    docs.append(doc)

# Write data to the database with write acknowledgment of w=2
start_time = time.time()
for doc in docs:
    db.write(doc, w=2)
write_time = time.time() - start_time
print(f"Data write time: {write_time} seconds")

# Update data in the database with write acknowledgment of w=2
update_docs = random.sample(docs, int(doc_count/2))
start_time = time.time()
for doc in update_docs:
    doc['data'] = ''.join(random.choices(string.ascii_lowercase, k=doc_size))
    db.write(doc, w=2)
update_time = time.time() - start_time
print(f"Data update time: {update_time} seconds")

# Read data from the database with read acknowledgment of r=2
read_docs = random.sample(docs, int(doc_count/2))
start_time = time.time()
for doc in read_docs:
    result = db.read(doc['_id'], r=2)
read_time = time.time() - start_time
print(f"Data read time: {read_time} seconds")

# Calculate the total time and print the performance benchmark
total_time = write_time + update_time + read_time
print(f"Total time: {total_time} seconds")
