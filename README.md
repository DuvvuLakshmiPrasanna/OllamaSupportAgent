# Offline Customer Support Chatbot with Ollama and Llama 3.2

An offline customer-support chatbot for e-commerce workflows, powered by Ollama and llama3.2:3b. The project compares zero-shot and one-shot prompting on 20 adapted customer queries and logs 40 scored responses for evaluation.

## Why This Project

Customer support often handles sensitive information such as order IDs, transaction issues, and account details. Sending these requests to third-party APIs can increase privacy, compliance, and operational risk. This project demonstrates a local-first alternative:

## Overview

This project builds and evaluates an offline customer support chatbot for a fictional e-commerce platform using Ollama and llama3.2:3b. It compares zero-shot and one-shot prompting across 20 adapted customer queries and logs 40 responses with manual scoring.

The key goal is to demonstrate how local LLM inference can support customer-service use cases while reducing privacy and compliance risk from external API dependency.

## Problem Context

Customer support conversations often include order IDs, payment issues, delivery disputes, and account details. In many organizations, sending this content to third-party hosted models raises data governance concerns. A local deployment strategy keeps inference inside the organization boundary and enables stronger control over sensitive data flows.

This project explores that trade-off with a practical experiment:

1. Run support prompts locally through Ollama.
2. Compare prompt strategies (zero-shot vs one-shot).
3. Score quality using a consistent rubric.
4. Summarize findings and limitations.

## Objectives

1. Build a functional Python client for Ollama API at localhost.
2. Use llama3.2:3b for response generation.
3. Test at least 20 e-commerce-related queries.
4. Produce both zero-shot and one-shot responses for each query.
5. Score outputs on Relevance, Coherence, and Helpfulness.

## Tech Stack

- Ollama (local model server)
- Llama 3.2 3B (llama3.2:3b)
- Python 3.x
- requests
- datasets

## End-to-End Flow

```text
chatbot.py
  -> loads prompt templates
  -> formats query into zero-shot and one-shot prompts
  -> POST http://localhost:11434/api/generate
  -> parses JSON response
  -> writes markdown table rows into eval/results.md
  -> user manually reviews and scores quality columns
```

## Repository Structure

```text
.
├── chatbot.py
├── data_prep.py
├── README.md
├── setup.md
├── report.md
├── requirements.txt
├── .gitignore
├── prompts/
│   ├── zero_shot_template.txt
│   └── one_shot_template.txt
├── eval/
│   └── results.md
└── scripts/
    ├── clean_project.ps1
    └── verify_submission.ps1
```

## Prompt Engineering Setup

### Zero-Shot Template

The zero-shot template provides role and policy constraints but no worked example.

### One-Shot Template

The one-shot template includes one hardcoded example query-response pair to guide structure, tone, and response style.

## Dataset and Query Adaptation

Queries are adapted from Ubuntu Dialogue Corpus style support scenarios into e-commerce intent categories.

Example adaptation logic:

- Network/device discovery issue -> shipping status tracking issue
- Installation/dependency failure -> discount code checkout failure

The adaptation demonstration script is in data_prep.py.

## Setup Guide

### 1. Install Ollama

Install Ollama for Windows from the official website, then verify:

```powershell
ollama --version
```

If PATH is not refreshed, use absolute executable path:

```powershell
"C:\Users\prasa\AppData\Local\Programs\Ollama\ollama.exe" --version
```

### 2. Pull Model

```powershell
ollama pull llama3.2:3b
```

### 3. Create and Activate Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Run Guide

### Standard Run

```powershell
python chatbot.py
```

### Optional Custom Run

```powershell
python chatbot.py --endpoint http://localhost:11434/api/generate --model llama3.2:3b --timeout 120 --output eval/results.md
```

### Expected Runtime Output

The script logs progress like:

```text
Processed query 1/20
...
Processed query 20/20
Saved evaluation log to: eval/results.md
```

## Evaluation Method

For each query, two outputs are generated:

- Zero-Shot response
- One-Shot response

Scoring rubric used in eval/results.md:

- Relevance (1-5): response addresses the query accurately
- Coherence (1-5): response is clear and well-formed
- Helpfulness (1-5): response provides actionable support value

## Results Summary

From eval/results.md:

| Metric      | Zero-Shot | One-Shot |
| ----------- | --------: | -------: |
| Relevance   |      3.90 |     4.65 |
| Coherence   |      4.25 |     4.95 |
| Helpfulness |      2.90 |     3.85 |

Interpretation:

- One-shot outperformed zero-shot across all dimensions.
- The strongest gain appears in helpfulness.
- One-shot prompting consistently produced more structured and helpful responses compared to zero-shot prompting.

## Utility Scripts

### scripts/clean_project.ps1

Removes local-only artifacts such as virtual environments, caches, build outputs, and coverage files.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\clean_project.ps1
```

### scripts/verify_submission.ps1

Validates required file structure and result completeness.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_submission.ps1
```

## Submission Checklist

Before final submission, verify:

1. chatbot.py runs successfully with local Ollama.
2. prompts directory has both templates.
3. eval/results.md has 40 rows (20 queries x 2 prompting methods).
4. Scores are filled for all required rubric columns.
5. README.md, setup.md, and report.md are present and consistent.

## Troubleshooting

- ollama command not found:
  - Restart terminal or VS Code.
  - Use absolute path executable command.
- Port binding error on 11434:
  - Ollama may already be running; do not start a second serve process.
- Connection refused in chatbot.py:
  - Confirm Ollama server is active and model is pulled.
- Slow generation:
  - CPU inference is expected to be slower than cloud GPU services.

## Limitations

- No real-time integration with order, payment, or shipping systems.
- Responses depend on template constraints and may miss policy edge cases.
- Small local model has reasoning limits for complex support workflows.

## Future Improvements

1. Add retrieval over policy documents for grounded answers.
2. Integrate safe internal tools for order and shipment lookups.
3. Add automated regression checks for prompt quality over time.

## Related Documents

- setup.md for focused setup steps
- report.md for detailed analysis and conclusion
- eval/results.md for full scored response log

## License

MIT
