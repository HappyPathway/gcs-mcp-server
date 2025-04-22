# Creating VS Code MCP Servers

## Overview

This guide details how to create a Model Context Protocol (MCP) server that integrates with Visual Studio Code. This template repository provides a foundation for building MCP servers that can be used by VS Code to extend AI capabilities through custom tools and services.

## Prerequisites

1. Python 3.8 or higher
2. Visual Studio Code
3. Basic understanding of the VS Code extension model

## Setting Up Your Development Environment

### 1. Getting Started with the Template

1. Create a new repository using this template:
   - Click "Use this template" on GitHub
   - Or clone and reinitialize:
   ```bash
   git clone https://github.com/your-org/mcp-server-template
   cd mcp-server-template
   ```

2. Set up your Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. Install the VS Code MCP extension (if not already installed)

## Implementation Guide

### 1. Basic Server Structure

The server implementation in `src/server.py` follows this pattern:

```python
from mcp.server import Server, tool

class MCPServer(Server):
    def __init__(self):
        super().__init__()
        # Initialize any required clients or resources

    @tool("Example tool")
    def example_tool(self, input_param: str) -> str:
        """A simple example tool.
        
        Args:
            input_param: Description of the input parameter
            
        Returns:
            The result of the tool's operation
        """
        return f"Processed: {input_param}"
```

### 2. Implementing Tools

Tools are the primary way your MCP server extends VS Code's AI capabilities. When implementing tools:

1. Use clear, descriptive names
2. Provide detailed docstrings
3. Define proper type hints
4. Handle errors gracefully
5. Return structured data when possible

Example tool patterns:

```python
class MyMCPServer(Server):
    @tool("Process file")
    def process_file(self, file_path: str) -> dict:
        """Process a file and return results.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dict containing processing results
        """
        # Implementation

    @tool("Search items")
    def search_items(self, query: str, max_results: int = 10) -> list:
        """Search for items matching the query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of matching items
        """
        # Implementation
```

### 3. Error Handling

Implement proper error handling for:
- Invalid inputs
- Resource access issues
- External service failures
- Timeouts
- VS Code integration errors

## VS Code Integration

### 1. Local Development

Configure VS Code to use your MCP server:

1. Create `.vscode/mcp.json`:
```json
{
  "servers": {
    "your-server-name": {
      "type": "stdio",
      "command": "python",
      "args": ["src/server.py"]
    }
  }
}
```

2. Set up launch configurations in `.vscode/launch.json` for debugging

### 2. Testing with VS Code

1. Use the Command Palette to:
   - List MCP servers
   - Check server status
   - Test tool invocations

2. Debug integration using:
   - VS Code's Debug Console
   - Output channels
   - Log files

## Best Practices

### 1. Tool Design

- Keep tools focused and atomic
- Use clear parameter names
- Provide good default values
- Return structured data
- Include proper error messages

### 2. Performance

- Implement caching where appropriate
- Use async/await for I/O operations
- Handle concurrent requests properly
- Monitor resource usage

### 3. Security

- Validate all inputs
- Handle sensitive data properly
- Implement proper access controls
- Follow VS Code security guidelines

## Testing

1. Unit Tests:
   - Test individual tools
   - Test error handling
   - Test edge cases

2. Integration Tests:
   - Test VS Code integration
   - Test concurrent operations
   - Test resource management

3. VS Code-specific Tests:
   - Test with different workspace types
   - Test with various VS Code settings
   - Test extension interop

## Deployment

### 1. Local Installation

Package your server for local installation:
- Create proper setup files
- Include dependencies
- Document installation steps

### 2. Distribution

If distributing your server:
- Package with pip/PyPI
- Provide clear installation instructions
- Include configuration examples
- Document requirements

## Contributing

1. Follow the code style guide
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## Additional Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [MCP Protocol Specification](https://github.com/microsoft/model-control-protocol)
- [Python MCP SDK Documentation](https://microsoft.github.io/model-control-protocol/python-sdk/)