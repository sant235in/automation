import random
import string
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import couchdb


def generate_random_data() -> Dict:
    return {
        "name": ''.join(random.choice(string.ascii_letters) for _ in range(10)),
        "age": random.randint(18, 60)
    }


def insert_data(db: couchdb.Database, num_docs: int):
    for i in range(num_docs):
        doc_id = str(uuid.uuid4())
        data = generate_random_data()
        db[doc_id] = data


def update_data(db: couchdb.Database, num_updates: int):
    for i in range(num_updates):
        doc_id = random.choice(list(db))
        data = db[doc_id]
        data["age"] = random.randint(18, 60)
        db[doc_id] = data


def delete_data(db: couchdb.Database, num_deletes: int):
    for i in range(num_deletes):
        doc_id = random.choice(list(db))
        del db[doc_id]


def read_data(db: couchdb.Database, num_reads: int):
    for i in range(num_reads):
        doc_id = random.choice(list(db))
        data = db[doc_id]
        print(f"Retrieved document with ID {doc_id}: {data}")


def run_concurrent_operations(db: couchdb.Database, num_docs: int, num_updates: int, num_deletes: int, num_reads: int):
    with ThreadPoolExecutor(max_workers=4) as executor:
        future1 = executor.submit(insert_data, db, num_docs)
        future2 = executor.submit(update_data, db, num_updates)
        future3 = executor.submit(delete_data, db, num_deletes)
        future4 = executor.submit(read_data, db, num_reads)

        start_time = time.time()
        future1.result()
        future2.result()
        future3.result()
        future4.result()
        end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Performed {num_docs} inserts, {num_updates} updates, {num_deletes} deletes, and {num_reads} reads in "
          f"{elapsed_time:.2f} seconds.")
    return elapsed_time


if __name__ == "__main__":
    couch = couchdb.Server("http://localhost:5984/")
    db_name = "mydatabase"
    if db_name not in couch:
        couch.create(db_name)
    db = couch[db_name]

    num_docs = 100
    num_updates = 10
    num_deletes = 5
    num_reads = 10

    run_concurrent_operations(db, num_docs, num_updates, num_deletes, num_reads)
