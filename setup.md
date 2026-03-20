# Setup and Run Guide

## 1. Install Ollama

1. Download and install Ollama from the official website for Windows.
2. Verify installation:

```powershell
ollama --version
```

## 2. Pull and Test Model

```powershell
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

Type `/bye` to exit the interactive session.

## 3. Create Python Environment

From the project root:

```powershell
python -m venv venv
venv\Scripts\activate
```

## 4. Install Python Dependencies

```powershell
pip install requests datasets
```

## 5. Run the Chatbot Evaluation Script

Ensure Ollama is running in the background, then execute:

```powershell
python chatbot.py
```

The script will:

- Load prompt templates from `prompts/`
- Process 20 adapted e-commerce queries
- Generate both zero-shot and one-shot responses
- Write markdown output to `eval/results.md`

## 6. Optional Custom Run

```powershell
python chatbot.py --endpoint http://localhost:11434/api/generate --model llama3.2:3b --timeout 120 --output eval/results.md
```

## 7. Troubleshooting

- **Connection refused**: Start/restart Ollama app, then retry.
- **Model not found**: Run `ollama pull llama3.2:3b`.
- **Slow responses**: CPU inference is expected to be slower than cloud GPU services.
- **`ollama` not recognized in terminal (Windows)**: Close and reopen VS Code/terminal to refresh PATH. If needed, run Ollama directly from `C:\Users\<your-user>\AppData\Local\Programs\Ollama\ollama.exe`.
