import os
from collections import namedtuple
import mimetypes
import re

STORAGE_CLASSES = ('STANDARD', 'NEARLINE', 'COLDLINE', 'ARCHIVE')

_Bucket_Metadata = namedtuple('Bucket_Metadata', [
    'id', 'name', 'storage_class', 'location', 'location_type', 
    'cors', 'default_event_based_hold', 'default_kms_key_name',
    'metageneration', 'public_access_prevention', 'retention_policy_effective_time',
    'retention_period', 'retention_policy_locked', 'requester_pays', 'self_link', 
    'time_created', 'versioning_enabled', 'labels'])

_Blob_Metadata = namedtuple('Blob_Metadata', [
    'id', 'blob_name', 'bucket_name', 'storage_class', 'file_size',
    'updated', 'generation', 'metageneration', 'etag', 'owner', 
    'component_count', 'crc32c', 'md5_hash', 'cache_control', 
    'content_type', 'content_disposition', 'content_encoding', 
    'content_language', 'metadata', 'meda_link', 'custom_time', 
    'temporary_hold', 'event_based_hold', 'retention_expiration_time'])

class GCStorage:
    def __init__(self, storage_client):
        self.client = storage_client

    def create_bucket(self, bucket_name, stoarge_class, location):
        bucket = self.client.bucket(bucket_name)
        bucket.storage_class = stoarge_class
        return self.client.create_bucket(bucket, location)

    def list_buckets(self):
        buckets = self.client.list_buckets()
        return [bucket.name for bucket in buckets]

    def get_bucket(self, bucket_name):
        return self.client.get_bucket(bucket_name)

    def get_bucket_metadata(self, bucket):
        bucket_metadata = _Bucket_Metadata(
            bucket.id,
            bucket.name,
            bucket.storage_class,
            bucket.location,
            bucket.location_type,
            bucket.cors,
            bucket.default_event_based_hold,
            bucket.default_kms_key_name,
            bucket.metageneration,
            bucket.iam_configuration.public_access_prevention,
            bucket.retention_policy_effective_time,
            bucket.retention_period,
            bucket.retention_policy_locked,
            bucket.requester_pays,
            bucket.self_link,
            bucket.time_created,
            bucket.versioning_enabled,
            bucket.labels
        )
        return bucket_metadata

    def add_bucket_labels(self, bucket, labels):
        if not isinstance(labels, dict):
            raise TypeError('Labels must be a dictionary')

        pattern = '[a-z0-9_-]+'
        for k, v in labels.items():
            if (re.sub(pattern, '', k) or re.sub(pattern, '', v)):
                raise ValueError("""Only hyphens (-), underscores (_), lowercase characters, and numbers are allowed. 
            Keys must start with a lowercase character. International characters are allowed.
                """.strip())
        bucket.labels = labels
        bucket.patch()
        return bucket

    def delete_bucket_labels(self, bucket):
        bucket.labels = {}
        bucket.patch()
        return bucket

    def list_blobs(self, bucket_name):
        return self.client.list_blobs(bucket_name)

    def get_blob_metadata(self, blob):
        blob_metadata = _Blob_Metadata(
            blob.id,
            blob.name,
            blob.bucket.name,
            blob.storage_class,
            blob.size,
            blob.updated,
            blob.generation,
            blob.metageneration,
            blob.etag,
            blob.owner,
            blob.component_count,
            blob.crc32c,
            blob.md5_hash,
            blob.cache_control,
            blob.content_type,
            blob.content_disposition,
            blob.content_encoding,
            blob.content_language,
            blob.metadata,
            blob.media_link,
            blob.custom_time,
            blob.temporary_hold,
            blob.event_based_hold,
            blob.retention_expiration_time
        )
        return blob_metadata

    def upload_file(self, bucket, blog_blob_destination, file_path):
        file_type = file_path.split('.')[-1]
        if file_type == 'csv':
            content_type = 'text/csv'
        elif file_type == 'psd':
            content_type = 'image/vnd.adobe.photoshop'
        else:
            content_type = mimetypes.guess_type(file_path)[0]
        blob = bucket.blob(blog_blob_destination)
        blob.upload_from_filename(file_path, content_type=content_type)
        return blob
    
    def download_file_by_blob_by_byte_range(self, bucket, blob_name, destination_folder, start_byte, end_byte):
        blob = bucket.blob(blob_name)
        blob.download_to_filename(destination_folder, start_byte, end_byte)
        print('File downloaded at {0}'.format(destination_folder))

    def download_file_by_blob(self, blob, destination_folder):
        if not os.path.exists(destination_folder):
            raise FileNotFoundError('Folder {0} not found.'.format(destination_folder))
        obj_metadata = self.get_blob_metadata(blob)
        blob_path = os.path.join(destination_folder, '/'.join(obj_metadata.blob_name.split('/')[:-1]))
        if not os.path.exists(blob_path):
            os.makedirs(blob_path)
        blob.download_to_filename(os.path.join(blob_path, obj_metadata.blob_name.split('/')[-1]))
        print('Download {0} to {1} finished'.format(obj_metadata.blob_name, blob_path))

    def download_files_by_bucket(self, bucket, destination_folder):
        if not os.path.exists(destination_folder):
            raise FileNotFoundError('Folder {0} not found.'.format(destination_folder))
        for blob in bucket.list_blobs():
            blob_metadata = self.get_blob_metadata(blob)
            blob_path = os.path.join(destination_folder, '/'.join(blob_metadata.blob_name.split('/')[:-1]))
            if not os.path.exists(blob_path):
                os.makedirs(blob_path)
            print('Downloading {0} to {1}'.format(blob_metadata.blob_name, blob_path))
            blob.download_to_filename(os.path.join(blob_path, blob_metadata.blob_name.split('/')[-1]))