#!/bin/bash

# Set the URL of the CouchDB server and database
COUCHDB_URL="http://localhost:5984"
COUCHDB_DB="mydatabase"

# Set the number of documents to generate
NUM_DOCS=100

# Generate random data and load it into the CouchDB database
for i in $(seq 1 $NUM_DOCS); do
  # Generate a random document ID
  DOC_ID=$(uuidgen)

  # Generate some random data
  DATA="{\"name\":\"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)\",\"age\":$(shuf -i 18-60 -n 1)}"

  # Load the data into the CouchDB database
  curl -s -X PUT "$COUCHDB_URL/$COUCHDB_DB/$DOC_ID" \
       -H "Content-Type: application/json" \
       -d "$DATA"
done

echo "Loaded $NUM_DOCS documents into the $COUCHDB_DB database."
