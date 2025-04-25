from typing import List, Dict, Optional, Any, Iterator, TypeVar, Callable, Union
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob
import logging
import os
import argparse

# Type aliases for better readability
GCSObject = Dict[str, Any]
BucketInfo = Dict[str, Optional[str]]

class GCSClient:
    """Wrapper around Google Cloud Storage client with helper methods"""
    def __init__(self):
        # Use application default credentials
        self.client = storage.Client()
        
    def get_bucket(self, bucket_name: str) -> Bucket:
        return self.client.bucket(bucket_name)

    def list_buckets(self) -> Iterator[Bucket]:
        return self.client.list_buckets()

    def list_objects(self, bucket_name: str, prefix: str = "", delimiter: str = "/") -> Iterator[Blob]:
        bucket = self.get_bucket(bucket_name)
        return bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    def read_object(self, bucket_name: str, object_path: str) -> Blob:
        bucket = self.get_bucket(bucket_name)
        return bucket.blob(object_path)

    def upload_object(self, bucket_name: str, object_path: str, content: str, content_type: str = "text/plain") -> Blob:
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_path)
        blob.upload_from_string(content, content_type=content_type)
        return blob

    def delete_object(self, bucket_name: str, object_path: str) -> None:
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(object_path)
        blob.delete()

    def copy_object(self, source_bucket: str, source_object: str, destination_bucket: str, destination_object: str) -> Blob:
        source_blob = self.get_bucket(source_bucket).blob(source_object)
        destination_bucket_obj = self.get_bucket(destination_bucket)
        return destination_bucket_obj.copy_blob(source_blob, destination_bucket_obj, destination_object)

    def list_object_versions(self, bucket_name: str, object_path: str) -> Iterator[Blob]:
        bucket = self.get_bucket(bucket_name)
        return bucket.list_blobs(prefix=object_path, versions=True)

def setup_logging() -> logging.Logger:
    """Configure and return logger"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

# Create FastMCP instance
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("GCS MCP Server")

# Initialize logging
logger = setup_logging()

# Initialize GCS client
try:
    gcs = GCSClient()
    # Verify we can access GCS
    next(gcs.list_buckets())
    logger.info("Successfully initialized GCS client with default credentials")
except Exception as e:
    logger.error(f"Failed to initialize: {str(e)}")
    raise

# Bucket Operations
@mcp.tool()
async def list_buckets() -> List[BucketInfo]:
    """List all GCS buckets in the project with their details"""
    logger.info("Listing GCS buckets")
    return [{
        "name": bucket.name,
        "created": bucket.time_created.isoformat() if bucket.time_created else None,
        "location": bucket.location,
        "storage_class": bucket.storage_class
    } for bucket in gcs.list_buckets()]

@mcp.tool()
async def create_bucket(bucket_name: str, location: str = "US", storage_class: str = "STANDARD") -> BucketInfo:
    """Create a new GCS bucket
    
    Args:
        bucket_name: Name of the new bucket
        location: Location for the bucket (default: "US")
        storage_class: Storage class for the bucket (default: "STANDARD")
    """
    logger.info(f"Creating bucket {bucket_name} in {location}")
    bucket = gcs.get_bucket(bucket_name)
    bucket.location = location
    bucket.storage_class = storage_class
    bucket.create()
    return {
        "name": bucket.name,
        "created": bucket.time_created.isoformat() if bucket.time_created else None,
        "location": bucket.location,
        "storage_class": bucket.storage_class
    }

@mcp.tool()
async def delete_bucket(bucket_name: str, force: bool = False) -> bool:
    """Delete a GCS bucket
    
    Args:
        bucket_name: Name of the bucket to delete
        force: If True, delete all objects in the bucket first
    """
    logger.info(f"Deleting bucket {bucket_name}")
    bucket = gcs.get_bucket(bucket_name)
    
    if force:
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()
    
    bucket.delete()
    return True

# Object Operations
@mcp.tool()
async def get_bucket_objects(bucket_name: str, prefix: str = "", delimiter: str = "/") -> List[GCSObject]:
    """List objects in a GCS bucket with optional prefix filter
    
    Args:
        bucket_name: Name of the GCS bucket
        prefix: Optional prefix to filter objects (default: "")
        delimiter: Optional delimiter for hierarchy (default: "/")
    """
    logger.info(f"Listing objects in bucket {bucket_name} with prefix {prefix}")
    blobs = gcs.list_objects(bucket_name, prefix=prefix, delimiter=delimiter)
    
    results: List[GCSObject] = []
    for blob in blobs:
        results.append({
            "name": blob.name,
            "size": blob.size,
            "updated": blob.updated.isoformat() if blob.updated else None,
            "content_type": blob.content_type,
            "md5_hash": blob.md5_hash
        })
    return results

@mcp.tool()
async def read_object(bucket_name: str, object_path: str) -> str:
    """Read the contents of a GCS object
    
    Args:
        bucket_name: Name of the GCS bucket
        object_path: Path to the object within the bucket
    """
    logger.info(f"Reading object {object_path} from bucket {bucket_name}")
    blob = gcs.read_object(bucket_name, object_path)
    return blob.download_as_text()

@mcp.tool()
async def upload_object(bucket_name: str, object_path: str, content: str, content_type: str = "text/plain") -> GCSObject:
    """Upload content to a GCS object
    
    Args:
        bucket_name: Name of the bucket
        object_path: Path where to create the object
        content: Content to upload
        content_type: Content type of the object
    """
    logger.info(f"Uploading to {object_path} in bucket {bucket_name}")
    blob = gcs.upload_object(bucket_name, object_path, content, content_type)
    
    return {
        "name": blob.name,
        "size": blob.size,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "content_type": blob.content_type,
        "md5_hash": blob.md5_hash
    }

@mcp.tool()
async def delete_object(bucket_name: str, object_path: str) -> bool:
    """Delete an object from GCS
    
    Args:
        bucket_name: Name of the bucket
        object_path: Path to the object to delete
    """
    logger.info(f"Deleting object {object_path} from bucket {bucket_name}")
    gcs.delete_object(bucket_name, object_path)
    return True

@mcp.tool()
async def copy_object(
    source_bucket: str,
    source_object: str, 
    destination_bucket: str,
    destination_object: str
) -> GCSObject:
    """Copy an object from one location to another in GCS
    
    Args:
        source_bucket: Name of the source bucket
        source_object: Path to the source object
        destination_bucket: Name of the destination bucket
        destination_object: Path for the destination object
    """
    logger.info(f"Copying {source_bucket}/{source_object} to {destination_bucket}/{destination_object}")
    blob_copy = gcs.copy_object(source_bucket, source_object, destination_bucket, destination_object)
    
    return {
        "name": blob_copy.name,
        "size": blob_copy.size,
        "updated": blob_copy.updated.isoformat() if blob_copy.updated else None,
        "content_type": blob_copy.content_type,
        "md5_hash": blob_copy.md5_hash
    }

@mcp.tool()
async def list_object_versions(bucket_name: str, object_path: str) -> List[GCSObject]:
    """List all versions of an object if versioning is enabled
    
    Args:
        bucket_name: Name of the bucket
        object_path: Path to the object
    """
    logger.info(f"Listing versions of {object_path} in bucket {bucket_name}")
    blobs = gcs.list_object_versions(bucket_name, object_path)
    
    return [{
        "name": blob.name,
        "generation": blob.generation,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "size": blob.size,
        "md5_hash": blob.md5_hash
    } for blob in blobs if blob.name == object_path]

if __name__ == "__main__":
    # Run the server
    mcp.run()