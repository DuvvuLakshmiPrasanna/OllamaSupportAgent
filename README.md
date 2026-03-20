# Offline Customer Support Chatbot with Ollama and Llama 3.2

This project demonstrates how to run an e-commerce customer support chatbot entirely on local hardware using Ollama and the Llama 3.2 3B model. It compares zero-shot and one-shot prompting strategies across 20 realistic customer queries and records the results in a structured evaluation file.

## Project Overview

E-commerce companies collect a significant amount of personal data through their customer support channels. A customer asking about an order status shares an order number. A customer disputing a charge includes transaction details. Over a support queue of any meaningful size, routing all of that through a third-party API creates both regulatory exposure and a dependency on external availability.

Running a language model locally with Ollama sidesteps both problems. The model weights live on your machine, inference happens within your network perimeter, and no customer data leaves the system. The trade-off is raw capability: a 3B parameter model is smaller than large cloud models, so prompt design and policy grounding matter.

This project tests that question concretely. It runs 20 adapted Ubuntu Dialogue Corpus style queries through two prompt configurations and scores outputs on Relevance, Coherence, and Helpfulness. The results and analysis are in `eval/results.md` and `report.md`.

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
├── chatbot.py                   # Main script: runs all 20 queries, writes results
├── data_prep.py                 # Demonstrates Ubuntu Corpus loading and adaptation
├── README.md                    # This file
├── setup.md                     # Step-by-step installation and execution guide
├── report.md                    # Quantitative and qualitative analysis report
├── requirements.txt             # Python dependencies (requests, datasets)
├── .gitignore                   # Standard Python gitignore
├── prompts/
│   ├── zero_shot_template.txt   # System persona + query placeholder, no example
│   └── one_shot_template.txt    # System persona + worked example + query placeholder
└── eval/
	└── results.md               # 40-row evaluation table with scores
```

## Key Concepts

### What Ollama is and why it was chosen

Ollama is a tool for running open-weight language models locally via a simple HTTP API. It handles model serving behind a lightweight local endpoint and keeps integration simple for a requests-based Python client.

### What Llama 3.2 3B is and its constraints

Llama 3.2 3B is a small model variant that can run on typical developer hardware. It is practical for constrained support workflows, but less reliable than larger models for complex reasoning and policy edge cases.

### Zero-shot prompting

Zero-shot prompting sends only task instructions and the customer query, with no prior example. It relies on baseline instruction-following behavior.

### One-shot prompting

One-shot prompting includes one worked example before the actual query. This helps the model follow expected tone and response format.

## Dataset

The Ubuntu Dialogue Corpus is a large collection of multi-turn technical support conversations. In this project, it is used as a source pattern for query adaptation into e-commerce support scenarios.

Adaptation examples:

- "I cannot connect to the internet after upgrading the kernel" becomes "How do I track the shipping status of my recent order?"
- "I ran apt-get install and it failed with a dependency conflict" becomes "My discount code says invalid at checkout. What should I do?"

## Findings Summary

| Metric      | Zero-Shot Average | One-Shot Average |
| ----------- | ----------------- | ---------------- |
| Relevance   | 3.90              | 4.65             |
| Coherence   | 4.25              | 4.95             |
| Helpfulness | 2.90              | 3.85             |

One-shot prompting consistently outperformed zero-shot on this evaluation set, especially in helpfulness and instruction clarity.

## How to Run

Full instructions are in [setup.md](setup.md). For users who already have Ollama installed and model pulled:

```bash
git clone https://github.com/DuvvuLakshmiPrasanna/OllamaSupportAgent.git
cd OllamaSupportAgent
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python chatbot.py
```

Results are written to `eval/results.md`.

## Limitations and Future Work

Current limitations:

- No direct integration with real order management systems
- Responses depend on prompt policy context and can still miss edge-case precision
- CPU inference can be slower for large evaluation runs

Future improvements:

- Add retrieval over policy documents for stronger factual grounding
- Integrate safe backend tools for order lookup workflows
- Add automated evaluation scripts and confidence checks

## License

MIT
