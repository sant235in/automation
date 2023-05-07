import pymongo
import ssl

# Set the MongoDB connection parameters
HOST = "mongodb://localhost:27017"
TLS_CA_FILE = "path/to/ca.pem"
TLS_KEYFILE = "path/to/keyfile.pem"
TLS_KEYFILE_PASSWORD = "your_password"

# Create a TLS connection with authentication
client = pymongo.MongoClient(
    HOST,
    ssl_ca_certs=TLS_CA_FILE,
    ssl_keyfile=TLS_KEYFILE,
    ssl_keyfile_password=TLS_KEYFILE_PASSWORD,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
)

# Iterate over all non-system databases
for db in client.list_databases():
    if db['name'] not in ['admin', 'config', 'local']:

        # Switch to the current database
        database = client[db['name']]

        # List all users and their roles in the current database
        print(f"Database: {db['name']}")
        for user in database.command('usersInfo')['users']:
            print(f"User: {user['user']}, Roles: {user['roles']}")
