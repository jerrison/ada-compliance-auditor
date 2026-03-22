# Introduction


## What it is / what it does


RocketRide agent nodes let you run an "agent framework" (like LangChain or CrewAI) inside a pipeline. You wire them like any other node: feed them questions, get back answers, give them access to an LLM and optionally give them access to tools via the invoke lane. Agents operate as tools themselves, wire up an agent as a tool to create a hierarchical agent flow with task delegation. All agents operate the same way within our pipelines, the difference is the underlying framework.


The framework-specific agent nodes are:


- agent_langchain
- agent_crewai


## When should I use an agent node?


Use an agent node when you want a pipeline step that can:


- Use Multi-Step Reasoning to answer a question
- Sub-Agent delegation for complex flows where separation of concerns is necessary
- Tool calling Capability (if you connect tool providers)
- Use your chosen LLM provider node


If you just want "LLM in, answer out" without tool orchestration, a plain llm_* node is simpler.


## Inputs and Outputs


Agent nodes use:


| Lane | Direction | What it carries |
| --- | --- | --- |
| questions | in | Questions (from a chat source or a question node) |
| answers | out | Answer text |


## Configuration


### Configuration fields (agent nodes)


Both agent_crewai and agent_langchain support the same user-facing config field:


- You may add as many "instructions" fields as necessary for your pipeline/use case


| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| instructions | string | "" | These instruction fields provide extra guidance/steps for the agent's run. |


### Control connections (LLM + tools)


Agent nodes do not contain API keys themselves. Instead:


- To let the agent call an LLM, you connect an LLM node through invoke.
- To let the agent call tools, you connect one or more tool provider nodes through invoke.


## How do I use it? (Step-by-step)


This is the most common "agent chat" pipeline shape:


1. Add a chat source.
2. Add an agent node (agent_langchain or agent_crewai).
3. Connect chat.questions → agent.questions.
4. Add an LLM node (example: llm_openai) and connect the invoke lane to the agent.
5. Add tools nodes (example: MCP_client or HTTP_Request).
6. Add a response node that returns answers (response_answers) and connect agent.answers → response.answers.
7. Run the pipeline and chat.


### Minimal example (.pipe)


```
{  "project_id": "88ad3ef8-0828-4596-8aea-9df63a89d6f8",  "source": "chat_1",  "components": [    {      "id": "chat_1",      "provider": "chat",      "config": { "hideForm": true, "mode": "Source", "type": "chat", "parameters": {} }    },    {      "id": "agent_1",      "provider": "agent_crewai",      "config": { "instructions": "Output: \"hello world\"" },      "input": [{ "lane": "questions", "from": "chat_1" }]    },    {      "id": "llm_openai_1",      "provider": "llm_openai",      "config": {        "profile": "openai-5-2",        "openai-5-2": { "apikey": "${ROCKETRIDE_OPENAI_KEY}" }      },      "control": [{ "classType": "llm", "from": "agent_1" }]    },    {      "id": "response_answers_1",      "provider": "response_answers",      "config": { "laneName": "answers" },      "input": [{ "lane": "answers", "from": "agent_1" }]    }  ]}
```


## Common use cases


- Tool-using chat assistant: connect a tool provider (example: mcp_client) so the agent can call tools during the conversation.
