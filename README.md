# DLP
This is in addition to the [solution](https://cloud.google.com/solutions/automating-classification-of-data-uploaded-to-cloud-storage) described.
Code in deidentify_with_mask.py includes adding code to retrieve data from Sensitive Bucket and masking them with characters 

Prerequisites
1) Create bucket YOUR_MASKED_BUCKET
2) Create cloud functions with Trigger from YOUR_SENSITIVE_BUCKET
