import pymongo
import ssl

# Set the MongoDB connection parameters
HOST = 'localhost'
PORT = 27017
USERNAME = 'admin'
PASSWORD = 'password'
CA_FILE = '/path/to/ca.pem'
KEY_FILE = '/path/to/keyfile.pem'
KEY_FILE_PASSWORD = 'password'

# Create a TLS connection to MongoDB
client = pymongo.MongoClient(HOST, PORT, username=USERNAME, password=PASSWORD,
                             tls=True, tlsCAFile=CA_FILE, tlsCertificateKeyFile=KEY_FILE,
                             tlsCertificateKeyFilePassword=KEY_FILE_PASSWORD,
                             ssl_cert_reqs=ssl.CERT_REQUIRED)

# Iterate over all the databases and list their users and roles
for database in client.list_databases():
    # Switch to the current database
    db = client[database['name']]
    # List all the users and their roles in the current database
    for user in db.command('usersInfo')['users']:
        print(f"Database: {database['name']}, User: {user['user']}, Roles: {user['roles']}")
