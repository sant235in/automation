#!/bin/bash

# Set the CouchDB database URL and name
COUCHDB_URL="http://localhost:5984"
DB_NAME="mydatabase"

# Set the number of threads and requests for Apache Bench
NUM_THREADS=10
NUM_REQUESTS=1000

# Create the database if it doesn't already exist
curl -X PUT "$COUCHDB_URL/$DB_NAME"

# Generate a JSON file with random data to use for inserts and updates
cat <<EOF > data.json
{
  "name": "$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10)",
  "age": "$(shuf -i 18-80 -n 1)",
  "address": "$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 20)",
  "phone": "$(shuf -i 1000000000-9999999999 -n 1)"
}
EOF

# Run Apache Bench for inserts, updates, reads, and deletes
ab -n $NUM_REQUESTS -c $NUM_THREADS \
  -T "application/json" -p data.json \
  -k "$COUCHDB_URL/$DB_NAME" \
  > results.txt 2>&1 &

ab -n $NUM_REQUESTS -c $NUM_THREADS \
  -T "application/json" -p data.json \
  -k -X PUT "$COUCHDB_URL/$DB_NAME/$(shuf -i 1-1000 -n 1)" \
  >> results.txt 2>&1 &

ab -n $NUM_REQUESTS -c $NUM_THREADS \
  -T "application/json" \
  -k "$COUCHDB_URL/$DB_NAME/$(shuf -i 1-1000 -n 1)" \
  >> results.txt 2>&1 &

ab -n $NUM_REQUESTS -c $NUM_THREADS \
  -T "application/json" \
  -k -X DELETE "$COUCHDB_URL/$DB_NAME/$(shuf -i 1-1000 -n 1)" \
  >> results.txt 2>&1 &

# Wait for all Apache Bench processes to finish
wait

# Print the results
cat results.txt
