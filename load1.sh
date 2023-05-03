#!/bin/bash

# Set the URL of the CouchDB server and database
COUCHDB_URL="http://localhost:5984"
COUCHDB_DB="mydatabase"

# Set the number of requests to send
NUM_REQUESTS=1000

# Set the concurrency level (number of requests to send at once)
CONCURRENCY=10

# Perform the benchmark
ab -n $NUM_REQUESTS -c $CONCURRENCY "$COUCHDB_URL/$COUCHDB_DB/"
