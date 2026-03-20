# Offline Customer Support Chatbot with Ollama and Llama 3.2

An offline customer-support chatbot for e-commerce workflows, powered by Ollama and llama3.2:3b. The project compares zero-shot and one-shot prompting on 20 adapted customer queries and logs 40 scored responses for evaluation.

## Why This Project

Customer support often handles sensitive information such as order IDs, transaction issues, and account details. Sending these requests to third-party APIs can increase privacy, compliance, and operational risk. This project demonstrates a local-first alternative:

- model runs on local machine
- inference remains inside your network boundary
- no external LLM API dependency at runtime

The goal is not just to generate answers, but to evaluate prompt strategy quality in a controlled setup.

## Objectives

- Build a working offline chatbot client against Ollama REST API
- Compare zero-shot vs one-shot prompting behavior
- Score outputs on relevance, coherence, and helpfulness
- Document findings and limitations for production-readiness discussion

## Tech Stack

- Ollama (local model serving)
- Llama 3.2 3B (llama3.2:3b)
- Python
- requests
- datasets (Hugging Face)

## High-Level Architecture

```text
chatbot.py
  -> formats prompt with query
  -> POST /api/generate (Ollama)
  -> receives model response JSON
  -> appends scored row-ready output to eval/results.md
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

## Prompting Design

### Zero-Shot

Uses role instructions and policy context without example output.

### One-Shot

Adds one worked query-response example in the template to steer tone and structure.

## Dataset and Query Adaptation

The project adapts Ubuntu Dialogue Corpus style issues into e-commerce support queries. This preserves real support-like user intent while shifting domain context.

Example adaptations:

- Technical: internet/driver issue -> E-commerce: order tracking issue
- Technical: dependency conflict -> E-commerce: invalid discount code issue

See data_prep.py for demonstration logic.

## Evaluation Results Summary

Based on eval/results.md:

| Metric      | Zero-Shot | One-Shot |
| ----------- | --------: | -------: |
| Relevance   |      3.90 |     4.65 |
| Coherence   |      4.25 |     4.95 |
| Helpfulness |      2.90 |     3.85 |

Conclusion: one-shot prompting produced stronger performance across all three evaluation dimensions in this run.

## Run Instructions

For full setup, see setup.md.

Quick start:

```bash
git clone https://github.com/DuvvuLakshmiPrasanna/OllamaSupportAgent.git
cd OllamaSupportAgent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python chatbot.py
```

Output is written to eval/results.md.

## Operational Utilities

This repository includes practical scripts so workspace hygiene is functional, not only configuration-based.

- scripts/clean_project.ps1
  - removes local-only artifacts such as virtual environments, caches, build outputs, and coverage files

- scripts/verify_submission.ps1
  - checks required deliverables
  - validates evaluation completeness (at least 40 response rows and 20 unique query IDs)

Run before final commit:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\clean_project.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify_submission.ps1
git status
```

## Limitations

- No direct integration with live order/payment/tracking systems
- Accuracy depends on prompt policy context and model limitations
- CPU-only local inference can be slow for batch evaluations

## Future Improvements

- Add retrieval augmentation over policy documents
- Add tool-safe integrations for order and shipment lookup
- Add automated scoring and regression checks for prompt updates

## License

MIT
