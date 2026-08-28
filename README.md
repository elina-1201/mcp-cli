# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Google AI Studio (Gemini) API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

> This is a modified version of the  [MCP project code](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1773092562/cli_project.zip?response-content-disposition=attachment&Expires=1787913906&Signature=I9Zj6JMKSDSyam2Vr2LX4wPpbeHpJA2mTqczFTUh02yPEYeDqj3XRagxRDWiIx7jJAZv0H71DuojelCrfj5fmRprHq3Pm75GUUZ4tbt740EvduerVeyZQJ8sptImxPY4BcnL1ZpwPVL6mBEK~Ho8NyvGiP6GNRppXQZX6mr0ZsRFKx3llnzXylF5KyrRGQIhI9TdJx4FE6LRRxHRlBp4VkXRXH02bXDwSYqEtcV9Nl9FQoFdivGREwSc1WQMiBgu0SKiKzpyl48GPcIJbw-VuCdH7yfUyIohrj490eMrPcISMMxd~CS1LFL9Ktgwq8NGLrfkyUAHINzE5HpSuprTFQ__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ) from Anthropic's course, [Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol/),  edited to use a Google AI Studio API key instead of Claude API key.

## Prerequisites

- Python 3.10+
- Google AI Studio API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
GEMINI_MODEL="gemini-3.6-flash"  # Enter your Google AI Studio model
GEMINI_API_KEY=""                # Enter your Google AI Studio API key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install google-genai python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.
