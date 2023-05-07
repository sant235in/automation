import pymongo
import ssl

# Set the connection parameters
HOST = "localhost"
PORT = 27017
USERNAME = "admin"
PASSWORD = "password"
CAFILE = "/path/to/cafile.crt"
KEYFILE = "/path/to/keyfile.pem"
KEYFILE_PASSWORD = "keyfile_password"

# Connect to the MongoDB instance with TLS and a keyfile with password
ssl_context = ssl.create_default_context(cafile=CAFILE)
ssl_context.load_cert_chain(KEYFILE, password=KEYFILE_PASSWORD)
client = pymongo.MongoClient(host=HOST, port=PORT, ssl=True, ssl_context=ssl_context)
db = client.admin
db.authenticate(USERNAME, PASSWORD)

# Get a list of all the non-system databases
databases = client.list_database_names()
databases = [db_name for db_name in databases if db_name not in ['admin', 'config', 'local']]

# Loop through each database and list the users and their roles
for database in databases:
    # Switch to the current database
    db = client[database]
    
    # Get a list of all the users and their roles in the current database
    users = db.command({'usersInfo': 1})['users']
    
    # Loop through each user and print the database name, user name, and role name in CSV format
    for user in users:
        roles = [role['role'] for role in user['roles']]
        print(f"{database},{user['user']},{'|'.join(roles)}")
