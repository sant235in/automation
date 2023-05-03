import time
import random
import string
import uuid
import argparse

import requests


def generate_random_data():
    return {
        "name": ''.join(random.choice(string.ascii_letters) for _ in range(10)),
        "age": random.randint(18, 60)
    }


def load_data(db_url, db_name, num_docs):
    for i in range(num_docs):
        doc_id = str(uuid.uuid4())
        data = generate_random_data()
        url = f"{db_url}/{db_name}/{doc_id}"
        response = requests.put(url, json=data)
        if response.status_code != 201:
            print(f"Error: Failed to load document {i+1}.")
            return False
    return True


def run_benchmark(db_url, db_name, num_requests, concurrency):
    start_time = time.time()
    for i in range(num_requests):
        doc_id = str(uuid.uuid4())
        url = f"{db_url}/{db_name}/{doc_id}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Request {i+1} failed with status code {response.status_code}")
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_request = total_time / num_requests
    print(f"Completed {num_requests} requests in {total_time:.2f} seconds.")
    print(f"Average time per request: {avg_time_per_request:.4f} seconds.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CouchDB performance benchmarking tool")
    parser.add_argument("--url", type=str, default="http://localhost:5984",
                        help="URL of the CouchDB server")
    parser.add_argument("--db", type=str, default="mydatabase",
                        help="Name of the CouchDB database")
    parser.add_argument("--num-docs", type=int, default=100,
                        help="Number of documents to load into the database")
    parser.add_argument("--num-requests", type=int, default=1000,
                        help="Number of requests to send to the database")
    parser.add_argument("--concurrency", type=int, default=10,
                        help="Number of requests to send at once")
    args = parser.parse_args()

    if not load_data(args.url, args.db, args.num_docs):
        print("Error: Failed to load data into the database.")
        exit(1)

    run_benchmark(args.url, args.db, args.num_requests, args.concurrency)
