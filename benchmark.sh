#!/bin/bash

# Number of documents to insert/update/delete/read
num_docs=1000

# Number of threads to use for each operation
num_threads=10

# Base URL of CouchDB server
base_url=http://localhost:5984

# Name of the database
db_name=my_database

# Function to insert a document
insert_doc() {
    for i in $(seq 1 $num_docs); do
        curl -s -X POST -H "Content-Type: application/json" -d '{"name": "document_'$i'", "value": '$i'}' $base_url/$db_name &
    done
    wait
}

# Function to update a document
update_doc() {
    for i in $(seq 1 $num_docs); do
        curl -s -X GET $base_url/$db_name/document_$i | sed 's/"value": [0-9]*/"value": '$(($num_docs + $i))'/' | curl -s -X PUT -H "Content-Type: application/json" -d @- $base_url/$db_name/document_$i &
    done
    wait
}

# Function to delete a document
delete_doc() {
    for i in $(seq 1 $num_docs); do
        curl -s -X DELETE $base_url/$db_name/document_$i &
    done
    wait
}

# Function to read a document
read_doc() {
    for i in $(seq 1 $num_docs); do
        curl -s -X GET $base_url/$db_name/document_$i > /dev/null &
    done
    wait
}

# Measure the benchmarking performance
echo "Inserting $num_docs documents..."
time (seq $num_threads | xargs -I{} -P $num_threads bash -c 'insert_doc')

echo "Updating $num_docs documents..."
time (seq $num_threads | xargs -I{} -P $num_threads bash -c 'update_doc')

echo "Deleting $num_docs documents..."
time (seq $num_threads | xargs -I{} -P $num_threads bash -c 'delete_doc')

echo "Reading $num_docs documents..."
time (seq $num_threads | xargs -I{} -P $num_threads bash -c 'read_doc')
