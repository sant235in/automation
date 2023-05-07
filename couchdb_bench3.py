import couchdb
import random
import string
import time

# Establishing connection with CouchDB
couch = couchdb.Server('http://localhost:5984')
db_name = 'test_db'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Generating random data
def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))

doc_size = 1024 # 1KB document size
data_count = 1000 # Number of documents to be created

data = []
for i in range(data_count):
    record = {}
    record['name'] = random_string(10)
    record['age'] = random.randint(20, 60)
    record['email'] = random_string(10) + '@example.com'
    record['doc_size'] = "x" * doc_size
    data.append(record)

# Creating index
db.create_index(fields=['name'])

# Measuring CRUD operation performance
start = time.time()

for record in data:
    # Insert operation
    db.save(record)

for record in data:
    # Read operation
    db.get(record['_id'])

for record in data:
    # Update operation
    record['age'] = random.randint(20, 60)
    db.save(record)

for record in data:
    # Delete operation
    db.delete(record)

end = time.time()

print(f"Total time taken: {end-start} seconds")
