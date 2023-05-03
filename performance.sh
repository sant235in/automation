#!/bin/bash

NUM_DOCS=100
NUM_UPDATES=10
NUM_DELETES=5
NUM_READS=10

DB_HOST=localhost
DB_PORT=5984
DB_NAME=mydatabase

function generate_random_data() {
    local name=$(cat /dev/urandom | tr -dc 'a-zA-Z' | fold -w 10 | head -n 1)
    local age=$((RANDOM % 43 + 18))
    echo "{\"name\": \"$name\", \"age\": $age}"
}

function insert_data() {
    for i in $(seq 1 $NUM_DOCS); do
        local doc_id=$(uuidgen)
        local data=$(generate_random_data)
        curl -s -X PUT "http://$DB_HOST:$DB_PORT/$DB_NAME/$doc_id" \
            -H "Content-Type: application/json" \
            -d "$data" >/dev/null &
    done
}

function update_data() {
    for i in $(seq 1 $NUM_UPDATES); do
        local doc_id=$(curl -s -X GET "http://$DB_HOST:$DB_PORT/$DB_NAME/_all_docs?limit=1" | \
            jq -r '.rows[].id')
        local data=$(curl -s -X GET "http://$DB_HOST:$DB_PORT/$DB_NAME/$doc_id" | \
            jq '.age = '$((RANDOM % 43 + 18)))
        curl -s -X PUT "http://$DB_HOST:$DB_PORT/$DB_NAME/$doc_id" \
            -H "Content-Type: application/json" \
            -d "$data" >/dev/null &
    done
}

function delete_data() {
    for i in $(seq 1 $NUM_DELETES); do
        local doc_id=$(curl -s -X GET "http://$DB_HOST:$DB_PORT/$DB_NAME/_all_docs?limit=1" | \
            jq -r '.rows[].id')
        curl -s -X DELETE "http://$DB_HOST:$DB_PORT/$DB_NAME/$doc_id" >/dev/null &
    done
}

function read_data() {
    for i in $(seq 1 $NUM_READS); do
        local doc_id=$(curl -s -X GET "http://$DB_HOST:$DB_PORT/$DB_NAME/_all_docs?limit=1" | \
            jq -r '.rows[].id')
        curl -s -X GET "http://$DB_HOST:$DB_PORT/$DB_NAME/$doc_id" >/dev/null &
    done
}

start_time=$(date +%s.%N)

insert_data
update_data
delete_data
read_data

wait

end_time=$(date +%s.%N)

elapsed_time=$(echo "$end_time - $start_time" | bc)

echo "Performed $NUM_DOCS inserts, $NUM_UPDATES updates, $NUM_DELETES deletes, and $NUM_READS reads in $elapsed_time seconds."
