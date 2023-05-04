#!/bin/bash

ARTIFACTORY_URL="http://your-artifactory-url.com/artifactory"
REPO_KEY="your-repository-key"
USERNAME="your-username"
PASSWORD="your-password"
FILE_PATH="path/to/your/file"
FILE_NAME="your-file-name"

RESPONSE=$(curl -u ${USERNAME}:${PASSWORD} -X PUT "${ARTIFACTORY_URL}/${REPO_KEY}/${FILE_NAME}" \
-T "${FILE_PATH}/${FILE_NAME}" \
--write-out "%{http_code}\n" \
--silent)

if [ "${RESPONSE}" == "201" ]; then
    echo "File uploaded successfully."
else
    echo "File upload failed with response code ${RESPONSE}."
fi
