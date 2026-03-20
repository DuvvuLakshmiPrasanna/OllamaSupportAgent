# Offline Customer Support Chatbot with Ollama & Llama 3.2

## Overview

This project implements an offline customer support chatbot for an e-commerce platform using a locally hosted LLM. It compares zero-shot and one-shot prompting on 20 adapted customer queries and logs scored outputs for analysis.

## Tech Stack

- Ollama (local LLM server)
- Llama 3.2 (3B model) via `llama3.2:3b`
- Python (`requests`)
- HuggingFace `datasets`

## Features

- Fully offline chatbot workflow (no external LLM API calls)
- Zero-shot vs one-shot prompt comparison
- Evaluation log with manual scoring metrics
- Configurable endpoint/model/timeout/output via CLI flags

## Results

- 20 queries tested
- 40 responses generated (Zero-Shot + One-Shot)
- One-shot prompting performed better overall in structure and helpfulness

## Repository Structure

- `chatbot.py`
- `README.md`
- `setup.md`
- `report.md`
- `requirements.txt`
- `prompts/zero_shot_template.txt`
- `prompts/one_shot_template.txt`
- `eval/results.md`

## Run

```bash
python chatbot.py
```

## Optional Run

```bash
python chatbot.py --model llama3.2:3b --endpoint http://localhost:11434/api/generate --timeout 120 --output eval/results.md
```

## Notes

- All inference runs locally through Ollama.
- No customer data is sent to third-party model APIs.
