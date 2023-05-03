import random
import string
import time
import uuid

import couchdb


def generate_random_data():
    return {
        "name": ''.join(random.choice(string.ascii_letters) for _ in range(10)),
        "age": random.randint(18, 60)
    }


def insert_data(db, num_docs):
    start_time = time.time()
    for i in range(num_docs):
        doc_id = str(uuid.uuid4())
        data = generate_random_data()
        db[doc_id] = data
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Inserted {num_docs} documents into the database in {elapsed_time:.2f} seconds.")
    return elapsed_time


def update_data(db, num_docs):
    start_time = time.time()
    for i in range(num_docs):
        doc_id = random.choice(list(db))
        data = db[doc_id]
        data["age"] = random.randint(18, 60)
        db[doc_id] = data
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Updated {num_docs} documents in the database in {elapsed_time:.2f} seconds.")
    return elapsed_time


def read_data(db, num_docs):
    start_time = time.time()
    for i in range(num_docs):
        doc_id = random.choice(list(db))
        data = db[doc_id]
        print(f"Retrieved document with ID {doc_id}: {data}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Retrieved {num_docs} documents from the database in {elapsed_time:.2f} seconds.")
    return elapsed_time


if __name__ == "__main__":
    couch = couchdb.Server("http://localhost:5984/")
    db_name = "mydatabase"
    if db_name not in couch:
        couch.create(db_name)
    db = couch[db_name]

    num_docs = 100
    insert_time = insert_data(db, num_docs)

    num_updates = 10
    update_time = update_data(db, num_updates)

    num_reads = 10
    read_time = read_data(db, num_reads)

    print(f"Total elapsed time: {insert_time + update_time + read_time:.2f} seconds.")
