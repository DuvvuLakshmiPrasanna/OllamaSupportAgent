# Offline Customer Support Chatbot with Ollama and Llama 3.2

This project demonstrates how to run an e-commerce customer support chatbot entirely on local hardware using Ollama and the Llama 3.2 3B model. It compares zero-shot and one-shot prompting strategies across 20 realistic customer queries and records the results in a structured evaluation file.

## Project Overview

E-commerce companies collect a significant amount of personal data through customer support channels. Routing all support interactions through third-party APIs can create regulatory risk and operational dependency. Running a local LLM with Ollama avoids that by keeping model execution and customer data on local infrastructure.

This project evaluates that approach using 20 adapted support queries and two prompt styles:

- Zero-shot prompting
- One-shot prompting

Each generated response is scored on:

- Relevance
- Coherence
- Helpfulness

Detailed outputs are in `eval/results.md`, with analysis in `report.md`.

## Architecture

```text
+-----------------------+
|                       |
|   chatbot.py          |
| (Your Python Script)  |
|                       |
+-----------+-----------+
			| 1. Format prompt with query
			| 2. Construct JSON payload
			v
+-----------------------+
|   HTTP POST Request   |
| to http://localhost...|
+-----------+-----------+
			|
			v
+-----------------------+
|                       |
|   Ollama Server       |
| (Running Locally)     |
|                       |
+-----------+-----------+
			| 3. Pass prompt to model
			v
+-----------------------+
|                       |
|   Llama 3.2 Model     |
|   (Inference)         |
|                       |
+-----------+-----------+
			| 4. Generate response text
			v
+-----------------------+
|                       |
|   Ollama Server       |
|                       |
|                       |
+-----------+-----------+
			| 5. Package response in JSON
			v
+-----------------------+
|   HTTP 200 OK Response|
| with generated text   |
+-----------+-----------+
			| 6. Parse JSON
			| 7. Log response
			v
+-----------------------+
|                       |
|   eval/results.md     |
| (Output Log File)     |
|                       |
+-----------------------+
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
└── eval/
	└── results.md
```

## Key Concepts

### Ollama

Ollama runs open-weight LLMs locally via a simple HTTP API. It handles serving and model runtime setup with minimal friction.

### Llama 3.2 3B

The `llama3.2:3b` model is small enough to run on consumer hardware. It is efficient, but less capable than larger cloud models on complex reasoning tasks.

### Zero-shot Prompting

Zero-shot prompting asks the model to perform a task with instructions only, without examples.

### One-shot Prompting

One-shot prompting includes one demonstration example before the actual query to improve style and response structure.

## Dataset

The Ubuntu Dialogue Corpus is used as a source pattern for realistic support interactions. Queries were adapted from technical support style into e-commerce support scenarios.

Two adaptation examples:

- "I cannot connect to the internet after upgrading the kernel" -> "How do I track the shipping status of my recent order?"
- "apt-get install failed with dependency conflict" -> "My discount code says invalid at checkout. What should I do?"

## Findings Summary

| Metric      | Zero-Shot Average | One-Shot Average |
| ----------- | ----------------- | ---------------- |
| Relevance   | 3.90              | 4.65             |
| Coherence   | 4.25              | 4.95             |
| Helpfulness | 2.90              | 3.85             |

One-shot prompting consistently produced more structured and helpful responses compared to zero-shot prompting.

## How to Run

Full setup is documented in `setup.md`.

```bash
git clone https://github.com/DuvvuLakshmiPrasanna/OllamaSupportAgent.git
cd OllamaSupportAgent
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
# source venv/bin/activate
pip install -r requirements.txt
python chatbot.py
```

Results are written to `eval/results.md`.

## Limitations and Future Work

- The model does not access live order systems or real customer records.
- Policy-grounded retrieval can further reduce hallucination risk.
- Larger models or GPU inference can improve quality and speed.

## License

MIT
