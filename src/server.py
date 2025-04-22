from mcp.server.fastmcp import FastMCP
import logging
import anyio
from google.cloud import storage
from google.cloud.storage.blob import Blob
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create GCS client
storage_client = storage.Client()

# Create FastMCP server instance
mcp = FastMCP("GCS MCP Server")

@mcp.tool()
async def list_buckets() -> List[Dict[str, str]]:
    """List all GCS buckets in the project with their details"""
    logger.info("Listing GCS buckets")
    buckets = storage_client.list_buckets()
    return [{
        "name": bucket.name,
        "created": bucket.time_created.isoformat() if bucket.time_created else None,
        "location": bucket.location,
        "storage_class": bucket.storage_class
    } for bucket in buckets]

@mcp.tool()
async def get_bucket_objects(bucket_name: str, prefix: str = "", delimiter: str = "/") -> List[Dict[str, str]]:
    """List objects in a GCS bucket with optional prefix filter
    
    Args:
        bucket_name: Name of the GCS bucket
        prefix: Optional prefix to filter objects (default: "")
        delimiter: Optional delimiter for hierarchy (default: "/")
    """
    logger.info(f"Listing objects in bucket {bucket_name} with prefix {prefix}")
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    
    results = []
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
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    return blob.download_as_text()

@mcp.tool()
async def create_bucket(bucket_name: str, location: str = "US", storage_class: str = "STANDARD") -> Dict[str, str]:
    """Create a new GCS bucket
    
    Args:
        bucket_name: Name of the new bucket
        location: Location for the bucket (default: "US")
        storage_class: Storage class for the bucket (default: "STANDARD")
    """
    logger.info(f"Creating bucket {bucket_name} in {location}")
    bucket = storage_client.bucket(bucket_name)
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
    bucket = storage_client.bucket(bucket_name)
    
    if force:
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()
    
    bucket.delete()
    return True

@mcp.tool()
async def upload_object(bucket_name: str, object_path: str, content: str, content_type: str = "text/plain") -> Dict[str, str]:
    """Upload content to a GCS object
    
    Args:
        bucket_name: Name of the bucket
        object_path: Path where to create the object
        content: Content to upload
        content_type: Content type of the object
    """
    logger.info(f"Uploading to {object_path} in bucket {bucket_name}")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.upload_from_string(content, content_type=content_type)
    
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
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)
    blob.delete()
    return True

@mcp.tool()
async def copy_object(
    source_bucket: str,
    source_object: str,
    destination_bucket: str,
    destination_object: str
) -> Dict[str, str]:
    """Copy an object from one location to another in GCS
    
    Args:
        source_bucket: Name of the source bucket
        source_object: Path to the source object
        destination_bucket: Name of the destination bucket
        destination_object: Path for the destination object
    """
    logger.info(f"Copying {source_bucket}/{source_object} to {destination_bucket}/{destination_object}")
    source = storage_client.bucket(source_bucket).blob(source_object)
    dest_bucket = storage_client.bucket(destination_bucket)
    
    blob_copy = dest_bucket.copy_blob(
        source, dest_bucket, destination_object
    )
    
    return {
        "name": blob_copy.name,
        "size": blob_copy.size,
        "updated": blob_copy.updated.isoformat() if blob_copy.updated else None,
        "content_type": blob_copy.content_type,
        "md5_hash": blob_copy.md5_hash
    }

@mcp.tool()
async def list_object_versions(bucket_name: str, object_path: str) -> List[Dict[str, str]]:
    """List all versions of an object if versioning is enabled
    
    Args:
        bucket_name: Name of the bucket
        object_path: Path to the object
    """
    logger.info(f"Listing versions of {object_path} in bucket {bucket_name}")
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=object_path, versions=True)
    
    return [{
        "name": blob.name,
        "generation": blob.generation,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "size": blob.size,
        "md5_hash": blob.md5_hash
    } for blob in blobs if blob.name == object_path]

if __name__ == "__main__":
    # Run the server using stdio transport by default
    mcp.run()