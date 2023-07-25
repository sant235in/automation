import requests

# Function to fetch the revision ID of a document in CouchDB
def get_revision_id(db_url, doc_id):
    url = f"{db_url}/{doc_id}"
    response = requests.get(url)
    if response.status_code == 200:
        doc_data = response.json()
        return doc_data.get("_rev")
    else:
        print(f"Error: Unable to fetch the document with ID '{doc_id}'")
        return None

# Function to update a document in CouchDB using the revision ID
def update_document(db_url, doc_id, rev_id, new_data):
    url = f"{db_url}/{doc_id}"
    headers = {"Content-Type": "application/json"}
    data = new_data
    data["_rev"] = rev_id

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Document with ID '{doc_id}' updated successfully.")
    else:
        print(f"Error: Unable to update the document with ID '{doc_id}'")

# Example usage
if __name__ == "__main__":
    # Replace these values with your CouchDB URL and document ID
    couchdb_url = "http://localhost:5984/my_database"
    document_id = "your_document_id"

    # Get the current revision ID of the document
    rev_id = get_revision_id(couchdb_url, document_id)
    
    if rev_id:
        # Update the document with the new data (replace this with your desired update)
        new_data = {
            "title": "Updated Document",
            "content": "This document has been updated!"
        }
        update_document(couchdb_url, document_id, rev_id, new_data)
