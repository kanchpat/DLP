""" Copyright 2018, Google, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless  required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Authors: Kanchana Patlolla.
Date:    July 2019

"""

from google.cloud import dlp
from google.cloud import storage
from google.cloud import pubsub
from google.cloud.storage import Blob

import os

# ----------------------------
#  User-configurable Constants

PROJECT_ID = 'YOUR_PROJECT_ID'
SENSITIVE_BUCKET = 'YOUR_SENSITIVE_BUCKET'
MASKED_BUCKET = 'YOUR_MASKED_BUCKET'
MIN_LIKELIHOOD = 'POSSIBLE'
"""The maximum number of findings to report (0 = server maximum)"""
MAX_FINDINGS = 0
"""The infoTypes of information to match"""
"""For more info visit: https://cloud.google.com/dlp/docs/concepts-infotypes"""
INFO_TYPES = [
    'FIRST_NAME', 'PHONE_NUMBER', 'EMAIL_ADDRESS', 'US_SOCIAL_SECURITY_NUMBER'
]

# End of User-configurable Constants
# ----------------------------------

# Initialize the Google Cloud client libraries
dlp = dlp.DlpServiceClient()
storage_client = storage.Client()

def deidentify_with_mask(data,done):

    # Convert the project id into a full resource id.
    parent = dlp.project_path(PROJECT_ID)

    # Construct inspect configuration dictionary
    inspect_config = {
        'info_types': [{'name': info_type} for info_type in INFO_TYPES]
    }

    # Construct deidentify configuration dictionary
    deidentify_config = {
        'info_type_transformations': {
            'transformations': [
                {
                    'primitive_transformation': {
                        'character_mask_config': {
                            'masking_character': 'X',
                            'number_to_mask': 0
                        }
                    }
                }
            ]
        }
    }


    storage_client = storage.Client()
    bucket = storage_client.get_bucket(SENSITIVE_BUCKET)

    blobs = bucket.list_blobs()

    for blob in blobs:
        gcs_file = blob.download_as_string()
        #contents = gcs_file.readline()
        item = {'value': gcs_file}
         # Call the API
        response = dlp.deidentify_content(
        parent, inspect_config=inspect_config,
        deidentify_config=deidentify_config, item=item)    
        masked_item = response.item.value
        destination_bucket = storage_client.get_bucket(MASKED_BUCKET)
        masked_blob = Blob(blob.name,destination_bucket)
        masked_blob.upload_from_string(masked_item)
