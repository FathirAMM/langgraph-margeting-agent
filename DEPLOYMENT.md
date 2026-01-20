# Deployment Guide

This guide explains how to deploy and run the Multi-Agent Marketing System using Docker. Since this is an interactive Command Line Interface (CLI) application, it is best run in an interactive container environment.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- An OpenAI API Key (and optionally a Tavily API Key).

## 🐳 Docker Deployment

### 1. Build the Docker Image

Navigate to the root of the project directory and run the following command to build the image. We'll tag it `marketing-agent`.

```bash
docker build -t marketing-agent .
```

### 2. Prepare Environment Variables

You can pass environment variables directly in the command line or use an `.env` file.

**Option A: Using an `.env` file (Recommended)**

Ensure you have a `.env` file in your directory (do not commit this to version control):

```env
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

**Option B: Passing variables inline**

You will pass them using `-e` flags in the run command.

### 3. Run the Container

Because the application requires user input (it prompts for requests), you **must** run the container in interactive mode using the `-it` flags.

**Run with `.env` file:**

```bash
docker run -it --env-file .env -v $(pwd)/data:/app/data marketing-agent
```
*Note: We mount a volume to `/app/data` if you want to persist the SQLite checkpoint file outside the container. You might need to adjust `src/graph.py` config to save to `/app/data/checkpoints.sqlite` if you want persistence across container restarts.*

**Run with inline variables:**

```bash
docker run -it -e OPENAI_API_KEY="your-key" marketing-agent
```

## ☁️ Cloud Deployment

Since this is a CLI tool, "deployment" typically means running it on a server or locally. However, if you wish to run this in a cloud environment:

### Virtual Machine (AWS EC2, DigitalOcean Droplet, etc.)
1. SSH into your server.
2. Clone the repository.
3. Install Docker.
4. Follow the Docker Build and Run steps above.
5. You will interact with the agent via your SSH session.

### Container Platforms (ECS, Kubernetes)
*Not recommended for this specific version.*
This application expects interactive standard input (`stdin`). Most serverless or container orchestration platforms (like AWS Fargate or Kubernetes deployments) are designed for long-running services (APIs) or batch jobs, not interactive CLIs.

To deploy this as a service accessible via the web, the `main.py` would need to be refactored into a web server (using FastAPI or Streamlit) that exposes endpoints or a UI for the user input.

## 💾 Persistence

By default, the `SqliteSaver` saves the conversation state to a local file (`checkpoints.sqlite`). Inside a Docker container, this file is ephemeral (lost when the container stops).

To persist state:
1. Mount a volume when running Docker: `-v $(pwd):/app`.
2. Or configure the application to write to a specific volume path.

## 🛠️ Troubleshooting

**Error: `EOFError: EOF when reading a line`**
- **Cause:** You likely forgot the `-it` flags. Docker is running without an interactive terminal, so `input()` fails immediately.
- **Fix:** Add `-it` to your docker run command.

**Error: `pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings`**
- **Cause:** The `OPENAI_API_KEY` is missing.
- **Fix:** Ensure you are passing the environment variable correctly via `.env` or `-e`.
