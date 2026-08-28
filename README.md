# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Google AI Studio (Gemini) API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

> This is a modified version of the  [MCP project code](https://cc.sj-cdn.net/instructor/4hdejjwplbrm-anthropic/assets/1773092562/cli_project.zip?response-content-disposition=attachment&Expires=1787913906&Signature=I9Zj6JMKSDSyam2Vr2LX4wPpbeHpJA2mTqczFTUh02yPEYeDqj3XRagxRDWiIx7jJAZv0H71DuojelCrfj5fmRprHq3Pm75GUUZ4tbt740EvduerVeyZQJ8sptImxPY4BcnL1ZpwPVL6mBEK~Ho8NyvGiP6GNRppXQZX6mr0ZsRFKx3llnzXylF5KyrRGQIhI9TdJx4FE6LRRxHRlBp4VkXRXH02bXDwSYqEtcV9Nl9FQoFdivGREwSc1WQMiBgu0SKiKzpyl48GPcIJbw-VuCdH7yfUyIohrj490eMrPcISMMxd~CS1LFL9Ktgwq8NGLrfkyUAHINzE5HpSuprTFQ__&Key-Pair-Id=APKAI3B7HFD2VYJQK4MQ) from Anthropic's course, [Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol/),  edited to use a Google AI Studio API key instead of Claude API key.

## Prerequisites

- Python 3.10+
- Google AI Studio API Key

## Setup

### Step 1: Create a Google AI Studio API key

The API key is free — no payment method or paid plan is required.

1. Go to [Google AI Studio](https://aistudio.google.com/) and sign in with your Google account.

2. Click **Get API key** (or open the [API keys page](https://aistudio.google.com/apikey) directly).

3. Click **Create API key**.

4. If you haven't used Google Cloud before, you may be asked to select or create a Google Cloud project. Pick the suggested default project (or create a new one) and continue.

5. Copy the generated API key and keep it safe. It is shown only once at creation time (you can still view or delete it later from the API keys page).

> **Tip:** The key is a secret. Never commit it to a repository or share it publicly. The `.env` file you create in Step 2 is already listed in `.gitignore`.

*If you had problem following the text setup above, here's a video walkthrough:*

📺 **[Watch the tutorial on YouTube](https://youtu.be/mtpIhr21mHA)**


### Step 2: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
GEMINI_MODEL="gemini-3.1-flash-lite"  # Enter your Google AI Studio model
GEMINI_API_KEY=""                # Enter your Google AI Studio API key
```

2. Paste the API key you copied in Step 1 as the value of `GEMINI_API_KEY`.

> **Note:** Models can become unavailable over time, and you may also reach request rate limits. If the model set in `GEMINI_MODEL` stops working (e.g. returns an error or is no longer listed), or if you hit the rate limit, replace it with another currently available model. You can find the full list of available models on the [Google AI Studio models page](https://ai.google.dev/gemini-api/docs/models).

### Step 3: Install dependencies

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

### Step 4: Test your API key

Before running the full chat, you can verify that your API key and model are working with the included `test_api.py` script.

The test loads `.env`, checks that both variables are set, and makes a single minimal query to the Gemini API — it asks the model to just say "OK" and prints the response. This confirms two things:

- Your API key is valid and the request actually reaches Google.
- The model set in `GEMINI_MODEL` exists and is correct.

Run it with:

```bash
uv run test_api.py            # with uv
```
 or
```bash
.venv/bin/python test_api.py  # without uv
```

If a response is printed, the key works. To go a step further, you can open your [Google AI Studio dashboard](https://aistudio.google.com/) and confirm that a request was sent from your key.

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