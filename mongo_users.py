import ssl
from pymongo import MongoClient

# Set the MongoDB connection parameters
HOST="localhost"
PORT="27017"
USERNAME="admin"
PASSWORD="password"

# Set the SSL/TLS options
CA_CERT="/path/to/ca.crt"
CERTFILE="/path/to/client.pem"
KEYFILE="/path/to/client.pem"
SSL=True

# Create a MongoClient with SSL/TLS options
if SSL:
    client = MongoClient(HOST, PORT, ssl=True, ssl_ca_certs=CA_CERT, ssl_certfile=CERTFILE, ssl_keyfile=KEYFILE)
else:
    client = MongoClient(HOST, PORT)

# Authenticate with the admin user
client.admin.authenticate(USERNAME, PASSWORD)

# Get a list of all the databases
databases = client.list_database_names()

# Loop through each database and list its users and roles
for database_name in databases:
    database = client[database_name]
    users = database.command("usersInfo")
    print(f"Database: {database_name}")
    for user in users["users"]:
        print(f"User: {user['user']}, Roles: {user['roles']}")

# Close the MongoClient connection
client.close()
