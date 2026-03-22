# LangChain


## What it is / what it does


agent_langchain is an agent node powered by LangChain. In a pipeline, it takes in questions and produces answers, optionally using an LLM and tools you connect to it.


For RocketRide pipeline wiring, lanes, and configuration, see RocketRide Agents.


## When to use it


Use agent_langchain when you want:


- A LangChain-based agent loop
- Tool access (if you connect tool providers)
- A node that works well in "tool calling" setups


## LangChain-specific behavior (what this node implements)


This node uses a small subset of LangChain's agent/tool concepts:


- Agent runtime: The driver uses LangChain's create_agent(...) and invokes the agent with the user prompt.


## Upstream docs (LangChain)


- LangChain (Python) concepts: agents
