# MCP Client


The MCP Client node (mcp_client) connects your pipeline to external Model Context Protocol servers and exposes their tools to agent nodes. It acts as a tool provider — agents can invoke tools discovered from the connected MCP server during their reasoning loop.


This complements the RocketRide MCP Server package (see the MCP Server section in the sidebar), which exposes RocketRide pipelines as MCP tools to external clients.


## Configuration


### Transport Selection


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| serverName | string | No | mcp | Identifier for the MCP server (used to namespace tools) |
| transport | string | No | stdio | Protocol type: stdio, sse, or streamable-http |


### STDIO Transport


| Field | Type | Notes |
| --- | --- | --- |
| commandLine | string | Full command line for spawning the MCP server process (preferred) |
| command | string | Command executable (legacy, use commandLine instead) |
| args | array | Command arguments (legacy, use commandLine instead) |
| env | object | Environment variables passed to the subprocess |


### HTTP Transports (SSE / Streamable-HTTP)


| Field | Type | Notes |
| --- | --- | --- |
| endpoint / sse_endpoint | string | HTTP(S) endpoint URL |
| bearer | string | Bearer token for the Authorization header |
| headers | object | Custom HTTP headers |


## Inputs and Outputs


### Input Channels


- Invoke — Tool invocation requests with parameters (connected from agent nodes).


### Output Channels


- Tool list — Discovered tools from the MCP server.
- Tool results — Results from tool invocations.


## How It Works


1. On startup, the node connects to the configured MCP server using the selected transport.
2. It discovers available tools via the MCP tools/list method and caches them.
3. Tools are namespaced as serverName.toolName (e.g. mcp.search_docs).
4. When an agent invokes a tool, the node validates the input against the tool's inputSchema and forwards the call to the MCP server.
5. Results are returned to the requesting agent.


## Key Details


- Supports three transport modes: STDIO (subprocess), SSE (HTTP long-polling), and Streamable-HTTP (streaming).
- Tools are discovered and cached at startup — no need to manually define tool schemas.
- Input is validated against each tool's inputSchema before invocation, including required field checks.
- Proper lifecycle management with initialize handshake (STDIO) and cleanup on shutdown.


## Common Use Cases


- Tool-augmented agents — Give agents access to external tools (web search, database queries, file operations) via MCP servers.
- Third-party integrations — Connect to any MCP-compatible server to extend agent capabilities.
- Multi-tool pipelines — Add multiple MCP Client nodes to give agents access to tools from several MCP servers.


## Example Pipeline


```
chat → agent_crewai → [invoke] → mcp_client (connects to external MCP server)                    → [invoke] → llm_openai         ↓    response_answers
```


The agent receives questions from the chat source, can call tools from the MCP server, uses the LLM for reasoning, and returns answers.


## Additional Resources


- Model Context Protocol Specification
- RocketRide MCP Server Documentation (see the MCP Server section in the sidebar)
