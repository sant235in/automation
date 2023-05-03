import requests
import time

# Set the URL of the CouchDB server and database
COUCHDB_URL = "http://localhost:5984"
COUCHDB_DB = "mydatabase"

# Set the number of requests to send
NUM_REQUESTS = 1000

# Set the concurrency level (number of requests to send at once)
CONCURRENCY = 10

# Send the requests and measure the performance
start_time = time.time()
for i in range(NUM_REQUESTS):
    response = requests.get(f"{COUCHDB_URL}/{COUCHDB_DB}")
    if response.status_code != 200:
        print(f"Error: Request {i+1} failed with status code {response.status_code}")
end_time = time.time()
total_time = end_time - start_time
avg_time_per_request = total_time / NUM_REQUESTS
print(f"Completed {NUM_REQUESTS} requests in {total_time:.2f} seconds.")
print(f"Average time per request: {avg_time_per_request:.4f} seconds.")
