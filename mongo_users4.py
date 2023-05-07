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

# Get a list of all the databases in the instance
databases = client.list_database_names()

# Iterate over each database and list its users and roles
for db_name in databases:
    # Skip the system databases
    if db_name not in ["admin", "config", "local"]:
        # Select the database and get its users
        db = client[db_name]
        users = db.command("usersInfo")
        # Iterate over each user and print its name and roles
        for user in users["users"]:
            roles = ",".join([role["role"] for role in user["roles"]])
            print(f"{db_name},{user['user']},{roles}")
