# Google Cloud Storage MCP Server Guide

## Overview

This MCP server provides tools for interacting with Google Cloud Storage (GCS) through VS Code's Copilot Chat. Built on the template-mcp-server foundation, it follows best practices for MCP server implementation while providing secure access to GCS operations.

## Features

- List buckets and objects
- Read and write object content
- Copy and delete objects
- Manage bucket lifecycle
- Support for object versioning
- Uses Application Default Credentials for authentication

## Prerequisites

1. Python 3.8 or higher
2. Visual Studio Code with MCP extension
3. Google Cloud Project with Storage enabled
4. Google Cloud CLI installed and configured (`gcloud`)

## Installation

### 1. Local Setup

1. Clone and set up the environment:
   ```bash
   git clone <repository-url>
   cd gcs-mcp-server
   python -m venv .venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. Configure Google Cloud authentication:
   ```bash
   gcloud auth application-default login
   ```
   This will set up your local environment to use Application Default Credentials.

### 2. Docker Setup

1. Build and run using Docker Compose (recommended):
   ```bash
   docker compose up --build
   ```

   This method will automatically:
   - Build the Docker image
   - Mount your Google Cloud credentials
   - Set up proper environment variables
   - Start the MCP server

2. Manual Docker setup:
   ```bash
   # Build the image
   docker build -t gcs-mcp-server .

   # Run the container
   docker run -v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/credentials.json:ro \
             -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/credentials.json \
             gcs-mcp-server
   ```

### 3. VS Code Configuration

Add the following to your VS Code settings (either User or Workspace):

```json
{
  "mcp": {
    "servers": {
      "gcs-mcp": {
        "type": "stdio",
        "command": "${userHome}/path/to/gcs-mcp-server/.venv/bin/python",
        "args": ["${userHome}/path/to/gcs-mcp-server/src/server.py"]
      }
    }
  }
}
```

## Available Tools

### Bucket Operations

1. `list_buckets`: List all GCS buckets in the project
2. `create_bucket`: Create a new bucket with specified configuration
3. `delete_bucket`: Delete a bucket (with optional force flag)

### Object Operations

1. `get_bucket_objects`: List objects in a bucket with optional prefix/delimiter
2. `read_object`: Read the contents of an object
3. `upload_object`: Upload content to a new or existing object
4. `delete_object`: Delete an object
5. `copy_object`: Copy objects between locations
6. `list_object_versions`: List all versions of an object

## Security Best Practices

1. Credential Management:
   - Use Application Default Credentials for authentication
   - Never commit credentials to version control
   - Support environment variables for CI/CD scenarios

2. Access Control:
   - Validate bucket and object names
   - Implement proper error handling
   - Log operations securely

3. Input Validation:
   - Sanitize all file paths and object names
   - Validate content types and sizes
   - Handle special characters properly

## Example Usage

Here are some example prompts for Copilot Chat:

1. List buckets:
   ```
   List all my GCS buckets
   ```

2. Read object:
   ```
   Show me the contents of file.txt from my-bucket
   ```

3. Upload content:
   ```
   Upload this text to my-bucket/new-file.txt: Hello, World!
   ```

## Troubleshooting

1. Credential Issues:
   - Verify Application Default Credentials are properly configured
   - Ensure Google Cloud CLI is installed and authenticated
   - Check environment variable configuration

2. Connection Problems:
   - Verify internet connectivity
   - Check Google Cloud API availability
   - Review server logs in VS Code Output panel

3. Tool Errors:
   - Enable debug logging for detailed error messages
   - Verify input parameters
   - Check access permissions

## Contributing

1. Follow template-mcp-server coding standards
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## Additional Resources

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Template MCP Server Guide](../template-mcp-server/docs/mcp-server-guide.md)
- [Model Context Protocol Specification](https://github.com/microsoft/model-control-protocol)