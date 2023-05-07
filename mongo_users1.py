import pymongo
import ssl

# Set the MongoDB connection parameters
HOST = "mongodb.example.com"
PORT = 27017
USERNAME = "admin"
PASSWORD = "password"
CA_CERT_PATH = "/path/to/ca.crt"
KEYFILE_PATH = "/path/to/client.pem"
KEYFILE_PASSWORD = "client_password"

# Create a TLS connection to the MongoDB instance
tls_context = ssl.create_default_context(cafile=CA_CERT_PATH)
tls_context.load_cert_chain(KEYFILE_PATH, password=KEYFILE_PASSWORD)
client = pymongo.MongoClient(HOST, PORT, username=USERNAME, password=PASSWORD, ssl=True, ssl_context=tls_context)

# Iterate over all databases and list all users and their assigned roles
for database in client.list_databases():
    db = client[database.name]
    for user in db.command("usersInfo"):
        print("Database: " + database.name + ", User: " + user['user'] + ", Roles: " + str(user['roles']))
