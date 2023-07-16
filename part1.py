import couchdb
import random
import string

# Change these variables according to your CouchDB configuration
COUCHDB_URL = 'http://localhost:5984'
DB_NAME = 'your_database_name'

# Function to generate random string for the document content
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Function to insert documents into the database
def insert_documents(db, num_documents):
    for i in range(num_documents):
        # Change 'partition_key' to the desired partition key field name
        partition_key = f'partition-{i % 10}'  # 10 partitions in this example
        content = generate_random_string(10)
        doc = {
            '_id': f'doc{i}',
            'partition_key': partition_key,
            'content': content,
        }
        db.save(doc)

# Main function
def main():
    couch = couchdb.Server(COUCHDB_URL)
    try:
        db = couch.create(DB_NAME)
    except couchdb.http.PreconditionFailed:
        db = couch[DB_NAME]

    num_documents = 100  # Change this to the desired number of documents
    insert_documents(db, num_documents)

    print(f'{num_documents} documents inserted into the database.')

if __name__ == '__main__':
    main()
