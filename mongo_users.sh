#!/bin/bash

# Set the MongoDB connection parameters
HOST="localhost"
PORT="27017"
DATABASE="admin"
USERNAME="admin"
PASSWORD="password"

# Connect to MongoDB and authenticate with the admin user
mongo --host $HOST:$PORT -u $USERNAME -p $PASSWORD --authenticationDatabase $DATABASE << EOF

# Switch to the database where the users are defined
use $DATABASE

# List all users and their roles
db.getUsers().forEach(function(user) {
  print("User: " + user.user + ", Roles: " + JSON.stringify(user.roles));
});

EOF
