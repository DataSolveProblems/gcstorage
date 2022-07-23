# Google Cloud Storage API v1

A lightweight Python package to simplify Google Cloud Storage operations.


## Installation

`pip install git+https://github.com/DataSolveProblems/gcstorage.git`


## Basic Usage

1. Create a Google Cloud Service Account

2. Enable Google Cloud Storage API

3. Start using gcstorage


## Examples

### 1. List buckets

```py
import os
from google.cloud import storage
from gcstorage import GCStorage, STORAGE_CLASSES

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_acct.json"
client = storage.Client()
gcs = GCStorage(client)
gcs.list_buckets()
```

### 2. Create a bucket

```py
my_bucket = gcs.create_bucket('<my bucket name>', storage_class=STORAGE_CLASSES[2], location='us')
```

### 3. Return bucket metadata

```py
my_bucket = gcs.get_bucket('my_bucket_y22')
bucket_metadata = gcs.get_bucket_metadata(my_bucket)
```

### 4. Add bucket labels

```py
my_bucket = gcs.get_bucket('my_bucket_y22')
gcs.add_bucket_labels(my_bucket, {'bucket_type': 'general', 'department': 'it'})
```

### 5. Delete bucket labels

```py
my_bucket = gcs.get_bucket('my_bucket_y22')
gcs.delete_bucket_labels(my_bucket)
```

### 6. List blobs in a bucket

```py
blobs = gcs.list_blobs(my_bucket.id)
for blob in blobs:
    print(blob.name)
```

### 7. Return a blob's metadata

```py
my_blob = my_bucket.get_blob(blob.name)
gcs.get_blob_metadata(my_blob)
```

### 8. Upload a file

```py
gcs.upload_file(my_bucket, 'object_destination', file_path)
```

### 9. Download a file

```py
gcs.download_file_by_blob(my_blob, '<file destination>')
```

### 10. Download files by a bucket

```py
gcs.download_files_by_bucket(my_bucket, '<file destination>')
```

### 11. Download file by byte range

```py
gcs.download_file_by_blob_by_byte_range(my_bucket, my_blob, '<file destination>', start_byte, end_byte)
```