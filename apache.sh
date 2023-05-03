#!/bin/bash

# Set the number of parallel requests
parallel_requests=10

# Set the number of iterations for each request type
insert_iterations=100
update_iterations=100
delete_iterations=100
read_iterations=100

# Generate random data
random_data=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n $parallel_requests)

# Insert random data in parallel
echo "Inserting data..."
parallel -j $parallel_requests "curl -X POST -H 'Content-Type: application/json' -d '{\"data\":\"{}\"}' http://localhost:5984/testdb -s" ::: $(seq 1 $insert_iterations)
echo "Data insertion complete."

# Update random data in parallel
echo "Updating data..."
parallel -j $parallel_requests "curl -X PUT -H 'Content-Type: application/json' -d '{\"data\":\"{}\"}' http://localhost:5984/testdb/{} -s" ::: $random_data ::: $(seq 1 $update_iterations)
echo "Data update complete."

# Delete random data in parallel
echo "Deleting data..."
parallel -j $parallel_requests "curl -X DELETE http://localhost:5984/testdb/{} -s" ::: $random_data ::: $(seq 1 $delete_iterations)
echo "Data deletion complete."

# Read random data in parallel
echo "Reading data..."
parallel -j $parallel_requests "curl -X GET http://localhost:5984/testdb/{} -s" ::: $random_data ::: $(seq 1 $read_iterations) > /dev/null
echo "Data reading complete."

# Measure performance using Apache Benchmark
ab -n $((parallel_requests * insert_iterations + parallel_requests * update_iterations + parallel_requests * delete_iterations + parallel_requests * read_iterations)) -c $parallel_requests http://localhost:5984/testdb
