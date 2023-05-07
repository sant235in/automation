import pymongo
import ssl

# Set the MongoDB connection parameters
HOST = "localhost"
PORT = 27017
USERNAME = "admin"
PASSWORD = "password"
TLS_CA_FILE = "/path/to/ca.crt"
TLS_KEY_FILE = "/path/to/client.pem"
TLS_KEY_PASSWORD = "key_password"

# Create a MongoDB client with TLS and authentication options
tls_context = ssl.create_default_context(cafile=TLS_CA_FILE)
tls_context.load_cert_chain(TLS_KEY_FILE, password=TLS_KEY_PASSWORD)
client = pymongo.MongoClient(host=HOST, port=PORT, tls=True, tlsCAFile=TLS_CA_FILE, tlsCertificateKeyFile=TLS_KEY_FILE, username=USERNAME, password=PASSWORD, authSource="admin", authMechanism="SCRAM-SHA-256", ssl_context=tls_context)

# Get the list of non-system databases
db_names = [db for db in client.list_database_names() if db not in ["admin", "config", "local"]]

# Iterate over each database and list its users and roles
for db_name in db_names:
    db = client[db_name]
    users = db.command("usersInfo")["users"]
    for user in users:
        username = user["user"]
        roles = user["roles"]
        print(f"{db_name}, {username}, {','.join(roles)}")
