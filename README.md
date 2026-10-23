# AI Question & Answering System

## Overview

This production-oriented Streamlit application answers questions with Google Gemini
model. It keeps the conversation in the current Streamlit session, supports follow-up
questions, and separates configuration, prompting, UI, service integration, and logging.

## Features

- ChatGPT-style Streamlit chat interface
- Multi-turn conversation history
- Configurable model and temperature
- Clear conversation control
- Loading indicator and friendly API errors
- Environment-based secret management
- Unit tests with a mocked Gemini client

## Architecture

- `app/config/settings.py`: validates environment-backed settings
- `app/services/gemini_service.py`: the only Gemini API integration
- `app/prompts/qa_prompt.py`: system prompt definition
- `app/main.py`: Streamlit presentation and session state
- `app/utils/logging_config.py`: standard-library logging setup

## Project structure

```text
question_answering_app/
├── app/
│   ├── config/settings.py
│   ├── prompts/qa_prompt.py
│   ├── services/gemini_service.py
│   ├── utils/logging_config.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── run.sh
```

## Prerequisites

- Python 3.10 or newer
- A Google Gemini API key

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `GEMINI_API_KEY`. You may also set
`GEMINI_MODEL` and `TEMPERATURE` (a number from 0 to 2):

```text
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-flash-latest
TEMPERATURE=0.2
```

Never commit `.env`.

## Run the application

macOS/Linux:

```bash
streamlit run app/main.py
```

Windows:

```powershell
python -m streamlit run app/main.py
```

Open the URL shown by Streamlit in your browser. Use **Clear Conversation** in the
sidebar to reset the current session.

## Run tests

```bash
pytest
```

Tests use mocks and do not require an API key or make network requests.

## Example questions

- What is the difference between a list and a tuple in Python?
- Explain how HTTP status codes work.
- What are the tradeoffs between SQL and NoSQL databases?
- Can you summarize the previous answer in three bullet points?

## Troubleshooting

- **`Python was not found` on Windows:** install Python 3.10 or newer from
  [python.org](https://www.python.org/downloads/windows/) and select **Add python.exe
  to PATH** during installation. Then open a new PowerShell window and verify:

  ```powershell
  python --version
  ```

  If Windows still redirects `python` to the Microsoft Store, open **Settings >
  Apps > Advanced app settings > App execution aliases** and turn off the `python.exe`
  and `python3.exe` aliases. Reopen PowerShell and retry the setup.

- **Virtual environment activation fails:** run the creation command first and only
  activate it after it succeeds:

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

  If PowerShell blocks the activation script, use this for the current terminal:

  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\.venv\Scripts\Activate.ps1
  ```

- **Missing API key:** copy `.env.example` to `.env` and add your key.
- **Authentication errors:** verify `GEMINI_API_KEY` and make sure the Gemini API is
  enabled for the associated Google project.
- **Quota errors:** review the Gemini API quota and billing settings for the
  associated Google project, then retry the question.
- **Invalid temperature:** set `TEMPERATURE` to a number between 0 and 2.
- **Dependency errors:** activate `.venv` and rerun
  `python -m pip install -r requirements.txt`.

The UI intentionally shows generic API errors and does not expose provider exception
details or secrets. Application logs contain event-level diagnostics, not full user
conversations or API keys.

## Security considerations

- API keys are loaded from `.env` and excluded by `.gitignore`.
- Do not put keys in source code, screenshots, issue reports, or logs.
- Restrict `.env` permissions in shared deployments.
- For production hosting, add authentication, rate limiting, usage monitoring, and
  centralized secret management.

## Stopping and deactivating

Press `Ctrl+C` in the terminal running Streamlit to stop the application. Deactivate
the virtual environment with:

```bash
deactivate
```

## Future enhancements

- Streaming token responses
- Persistent, authenticated conversation storage
- Rate limiting and usage budgets
- Retrieval-augmented answers from private documents
- Structured observability and deployment health checks
