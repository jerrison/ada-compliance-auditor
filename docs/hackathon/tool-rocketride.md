# RocketRide

- **Created:** March 21, 2026 9:22 AM
- **Link:** [rocketride.org](https://rocketride.org/)

> To enable oAuth for Google nodes within RocketRide, send an email to:
> - joe.maionchi@rocketride.ai
> - dmitrii.kataraev@rocketride.ai

> RocketRide is a developer-first platform for building and deploying AI pipelines from your IDE.
> - Visual pipeline builder (nodes + wiring)
> - High-performance engine designed for production workloads
> - Works with many model providers, vector DBs, and common processing steps

## What you'll use at the hackathon

- The IDE extension to build and run pipelines (the RocketRide sidebar in VS Code).
- A pipeline file (create a `.pipe` file) where you wire nodes together and configure inputs/outputs. [1](https://github.com/rocketride-org/rocketride-server)
- A server/engine runtime that executes your pipeline (local is easiest, Docker/on-prem is available). [2](https://github.com/rocketride-org/rocketride-server)

## Quick start (fastest path)

1. Install the RocketRide extension in your IDE (VS Code recommended). [1](https://github.com/rocketride-org/rocketride-server)
2. Open the RocketRide (rocket) panel.
3. Choose a server option when prompted:
   - **Local (recommended):** pulls the server into your IDE with minimal setup. [1](https://github.com/rocketride-org/rocketride-server)
   - **On-prem / Docker:** run the engine on your own hardware when you need control or data residency. [1](https://github.com/rocketride-org/rocketride-server)
4. Create a `.pipe` file and build your workflow (drag nodes, connect them, set params). [1](https://github.com/rocketride-org/rocketride-server)

## Running & testing your pipeline

- **Start with a tiny end-to-end flow:**
  - Input -> LLM call -> Output
- **Then add practical hackathon pieces:**
  - Document ingest (extract/OCR) -> chunk/embed -> vector DB -> RAG answer
  - PII redaction before retrieval if you are working with sensitive text
- Use deterministic prompts where you can so demos are repeatable.

## Deploy options (when you want to share a demo)

- **Docker:** build and run the engine on a server. [3](https://rocketride.org/)
  ```
  # Build (in repo dir on your server)
  docker build -f docker/Dockerfile.engine -t rocketride-engine .
  # Run on your server
  docker run -p 8080:8080 rocketride-engine
  ```
- **Cloud:** RocketRide Cloud is listed as coming soon. [3](https://rocketride.org/)

## SDK (optional)

If you want to call a pipeline from an app, you can use the TypeScript or Python SDKs. [3](https://rocketride.org/)

## Tips for a strong hackathon project

- Make RocketRide a core part of the system (not just a screenshot).
- Show your pipeline structure clearly: inputs, nodes, outputs, and why each step exists.
- Prefer one "wow" workflow over many half-finished ones.

## Links

- **Website:** https://rocketride.org
- **Engine repo:** https://github.com/rocketride-org/rocketride-server
