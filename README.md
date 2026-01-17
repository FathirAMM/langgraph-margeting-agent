# Multi-Agent Marketing System

A production-grade multi-agent system built with **LangGraph**, **LangChain**, and **OpenAI**. This system orchestrates a team of specialized AI agents to produce high-quality marketing content, from research to SEO optimization and visual design, all governed by a Supervisor and Compliance system.

## 🚀 Features

- **Supervisor Architecture**: A central LLM router (Supervisor) manages the workflow and delegates tasks.
- **Specialized Agents**:
  - 🕵️ **Senior Researcher**: Conducts deep web research and scraping.
  - ✍️ **Content Strategist**: Drafts engaging, formatted marketing content.
  - 🔍 **SEO Optimizer**: Analyzes and improves content for search engines.
  - 🎨 **Visual Designer**: Generates AI image prompts to match the content.
  - 🛡️ **Compliance Officer**: Enforces guardrails (formatting, safety, policy).
- **Rich CLI**: Professional, threaded command-line interface with status spinners and markdown rendering.
- **Persistence**: SQLite-backed checkpointing allows resuming conversation threads.
- **Guardrails**: Integrated content validation to ensure quality and safety.
- **Custom Tools**: Web scraper, SEO analyzer, and more.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This project requires Python 3.10+.*

3. **Configure Environment**:
   Copy the example environment file and add your API keys.
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in:
   - `OPENAI_API_KEY`: Required for agents.
   - `TAVILY_API_KEY`: Optional (if using Tavily search).

## 🏃 Usage

Run the main entry point:

```bash
python main.py
```

1. Enter a **Thread ID** (or press Enter for default) to maintain session state.
2. Enter your marketing request (e.g., "Write a blog post about the future of AI in healthcare").
3. Watch the agents work!

## 🏗️ Architecture

The system uses **LangGraph** to define a stateful graph where:
- **Nodes** are Agents (or the Supervisor).
- **Edges** define the flow of information.
- **State** is a shared dictionary containing the conversation history.

### The Workflow
1. **Supervisor** analyzes the request and routes to **Senior_Researcher**.
2. **Researcher** gathers data.
3. **Supervisor** routes to **Content_Strategist** to draft content.
4. **Supervisor** routes to **SEO_Optimizer** to refine.
5. **Supervisor** routes to **Visual_Designer** for assets.
6. **Supervisor** routes to **Compliance_Officer** for final checks.
7. **Compliance_Officer** approves or rejects (sending it back for revision).
8. **Supervisor** finishes the task.

## 🧪 Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## 📄 License

MIT License
