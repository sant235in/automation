import pymongo
import ssl

# Define the connection parameters
HOST = 'localhost'
PORT = 27017
USERNAME = 'admin'
PASSWORD = 'password'
CA_CERT = 'ca.pem'
KEYFILE = 'key.pem'
KEYFILE_PASSWORD = 'keyfile_password'

# Set up the TLS connection parameters
tls_options = {
    'ssl': True,
    'ssl_ca_certs': CA_CERT,
    'ssl_keyfile': KEYFILE,
    'ssl_keyfile_password': KEYFILE_PASSWORD
}

# Connect to the MongoDB instance
client = pymongo.MongoClient(HOST, PORT, username=USERNAME, password=PASSWORD, tls=tls_options)

# Get a list of all the databases in the instance
databases = client.list_database_names()

# Loop through each database and list the users and their roles
for database_name in databases:
    database = client[database_name]
    users = database.command('usersInfo')
    print(f'Users in database {database_name}:')
    for user in users['users']:
        print(f'User: {user["user"]}, Roles: {user["roles"]}')
