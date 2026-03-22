# CrewAI


## What it is / what it does


agent_crewai is an agent node powered by CrewAI. In a pipeline, it takes in questions and produces answers, optionally using an LLM and tools you connect to it.


For RocketRide pipeline wiring, lanes, and configuration, see RocketRide Agents.


## When to use it


Use agent_crewai when you want:


- A CrewAI-based agent loop


## CrewAI-specific behavior (what this node implements)


This node uses a subset of CrewAI's core concepts:


- Agent / Task / Crew: The driver builds a single Agent, wraps the user request into a Task, and runs a Crew.kickoff().


## Upstream docs (CrewAI)


- CrewAI documentation
