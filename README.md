# Creating a Python MCP Server: A Step-by-Step Guide

The Model Context Protocol (MCP) provides a standardized approach for connecting context sources to large language models (LLMs). This tutorial demonstrates how to build a functional MCP server using Python's MCP SDK, enabling you to expose data, tools, and templates to LLM applications.

## What is MCP?

MCP creates a bridge between LLM applications and external context sources. It allows you to modularize different aspects of LLM interactions:
- **Data provision** through resources (similar to read-only endpoints)
- **Action execution** via tools (comparable to API functions)
- **Template management** using prompts for reusable interactions

## Core MCP Components

MCP servers implement three fundamental building blocks, each serving different purposes:

| Component | Controlled By | Purpose | Common Uses |
|-----------|---------------|---------|-------------|
| **Prompts** | User | Interactive templates triggered by user selection | Command shortcuts, menu items |
| **Resources** | Application | Data managed by the client for LLM context | File content, API data |
| **Tools** | LLM | Functions the model can execute independently | Calculations, API calls, data modifications |

Understanding these distinctions helps you design effective MCP servers that properly separate concerns.

## Server Feature Advertising

MCP servers announce their capabilities during startup, allowing clients to adapt their behavior:

| Feature | Configuration Flag | What It Enables |
|---------|-------------------|-----------------|
| **prompts** | `listChanged` | Dynamic prompt template updates |
| **resources** | `subscribe`, `listChanged` | Data exposure with live updates |
| **tools** | `listChanged` | Function discovery and execution |
| **logging** | Default | Debug output configuration |
| **completion** | Default | Argument suggestion support |

## Getting Started

### Requirements

Ensure your environment includes:
- **Python 3.7+** (Python 3.11+ recommended)
- **pip** package manager
- **Node.js 18.x**

### Installation Options

Choose one of these installation methods:

**Standard pip installation:**
```bash
pip install "mcp[cli]"
```

**Using uv (recommended for project management):**
```bash
uv init mcp-server
cd mcp-server
uv add "mcp[cli]"
```

### Project Structure

Organize your project as follows:
```
mcp-server/
├── server.py
├── pyproject.toml (if using uv)
└── README.md
```

## Implementation

### Building Your Server

Create `server.py` with the following foundation:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Demo Server")

# Define a calculation tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Performs addition of two integers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of both numbers
    """
    return a + b

# Create a dynamic resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Generates a personalized greeting.
    
    Args:
        name: Person's name for the greeting
    
    Returns:
        Formatted greeting message
    """
    return f"Hello, {name}!"

# Add a prompt template
@mcp.prompt()
def review_code(code: str) -> str:
    """
    Creates a code review template.
    
    Args:
        code: Source code to review
    
    Returns:
        Formatted review prompt
    """
    return f"Please review this code:\n\n{code}"

# Server execution
if __name__ == "__main__":
    mcp.run()
```

## Testing Your Server

### Using the Development Inspector

The most efficient way to test your server is through the built-in development interface:

```bash
mcp dev server.py
```

This command:
- Launches your server with live reloading
- Opens a web interface at `http://localhost:6274/`
- Provides interactive testing capabilities

### Inspector Configuration

In the Inspector interface, configure the transport settings:

```
Transport Type: STDIO  
Command: python  
Arguments: server.py
```

Click **Connect** to establish the connection.

### Testing Each Component

#### Tool Testing
1. Navigate to the **Tools** section
2. Select the `add` tool
3. Input test values (e.g., `a = 10`, `b = 15`)
4. Execute and verify the result (`25`)

#### Resource Testing
1. Go to **Resources** → **Resource Templates**
2. Select `get_greeting`
3. Enter a name (e.g., `Alice`)
4. Click **Read Resource**
5. Verify the response: `"Hello, Alice!"`

#### Prompt Testing
1. Access **Prompts** → **List prompts**
2. Select `review_code`
3. Input sample code: `print(1+1)`
4. Execute to see the formatted prompt output

Run this in a separate terminal while your server is active.

## Understanding Server Behavior

When you run `python server.py` directly, the server appears inactive because it uses **stdio transport** and waits for client connections. This is normal behavior - the server needs a client (like the Inspector or your custom client) to interact with it.
