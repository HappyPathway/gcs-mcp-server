# Python MCP Server Template

A template repository for creating Model Context Protocol (MCP) servers using Python with stdio transport.

## Overview

This template provides a standardized setup for building MCP servers that integrate with VS Code. It uses:
- Python with the official MCP server library
- Standard input/output (stdio) for communication
- VS Code integration for seamless development

## Features

- Example MCP tools implementation with decorators
- VS Code development environment support
- Simple stdio-based transport for reliable local development
- Easy debugging with VS Code's Python debugger

## Getting Started

1. Use this template repository to create your new MCP server project
2. Create and activate a Python virtual environment
3. Install dependencies from requirements.txt
4. Customize the MCP tools in the Python code
5. Test locally with VS Code

## Project Structure

```
.
├── src/                    # Python source code
│   └── server.py          # MCP server implementation
├── .vscode/               # VS Code configuration
└── README.md              # Project documentation
```

## Customization

To implement your own MCP server:

1. Modify the Python code to add your custom tools using the `@tool` decorator
2. Update requirements.txt if additional dependencies are needed
3. Configure your VS Code workspace settings

## Development

1. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. Configure VS Code:
   - Create .vscode/mcp.json with stdio configuration
   - Set up Python interpreter in VS Code
   - Use the integrated terminal for running commands
   - Debug your MCP server using VS Code's Python debugger

3. Test your MCP server:
   - Use VS Code's built-in MCP server testing capabilities
   - Debug with breakpoints and VS Code's debug console
   - Monitor stdio communication in the output panel

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Your chosen license]