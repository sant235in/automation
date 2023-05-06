#!/bin/bash

# Set the MongoDB connection parameters
HOST="localhost"
PORT="27017"
USERNAME="admin"
PASSWORD="password"

# Get the list of all databases
DATABASES=$(mongo --host $HOST:$PORT --authenticationDatabase admin --username $USERNAME --password $PASSWORD --quiet --eval "db.adminCommand({listDatabases: 1})" | jq -r '.databases[].name')

# Iterate over each database and list all users and their roles
for db in $DATABASES
do
  # Skip the system databases
  if [[ $db == "admin" || $db == "local" || $db == "config" ]]; then
    continue
  fi

  # Get the list of all users and their roles
  USERS=$(mongo --host $HOST:$PORT --authenticationDatabase admin --username $USERNAME --password $PASSWORD --quiet $db --eval "db.runCommand({usersInfo: 1})" | jq -r '.users[] | "\(.user),\(.roles | map(select(.role != "") | .role) | join(","))"')
  #USERS=$(mongo --host $HOST:$PORT --authenticationDatabase admin --username $USERNAME --password $PASSWORD --quiet $db --eval "db.getUsers()" | jq -r '.[].user' | xargs -I {} mongo --host $HOST:$PORT --authenticationDatabase admin --username $USERNAME --password $PASSWORD --quiet $db --eval "printjson(db.getUser('{}'))" | jq -r '"User: \(.user), Roles: \(.roles | map(.role) | join(", "))"')

  # Print the database name and the list of users and their roles
  echo "Database: $db"
  echo "$USERS"
  echo ""
done
