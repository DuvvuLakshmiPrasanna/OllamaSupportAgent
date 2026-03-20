from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

import requests

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"
DEFAULT_TIMEOUT_SECONDS = 120

PROJECT_ROOT = Path(__file__).resolve().parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
EVAL_DIR = PROJECT_ROOT / "eval"

ZERO_SHOT_TEMPLATE_PATH = PROMPTS_DIR / "zero_shot_template.txt"
ONE_SHOT_TEMPLATE_PATH = PROMPTS_DIR / "one_shot_template.txt"
DEFAULT_RESULTS_PATH = EVAL_DIR / "results.md"

# Adapted to e-commerce context from the style of support issues in Ubuntu Dialogue Corpus.
ADAPTED_QUERIES: List[str] = [
    "How do I track the shipping status of my recent order?",
    "My discount code says invalid at checkout. What should I do?",
    "I received the wrong item in my package. How can I replace it?",
    "Can I change my delivery address after placing the order?",
    "Can I return a dress if I removed the tags but never wore it?",
    "How long does it take to get my refund after I return an item?",
    "I want to cancel my order, but it already says packed.",
    "My order is marked delivered, but I did not receive it.",
    "Payment failed once, then I got charged twice. Can you help?",
    "Can I add gift wrapping after the order has been placed?",
    "I need to exchange shoes for a different size.",
    "Why are my loyalty points missing from my account after purchase?",
    "When will my preorder item be shipped?",
    "How can I download the invoice for my last order?",
    "Do you offer international shipping and customs support?",
    "One item from my order arrived, but another is still pending.",
    "My account is locked after too many login attempts.",
    "How do I unsubscribe from promotional emails?",
    "The product stopped working in two weeks. Can I claim warranty?",
    "Can I use two coupons in the same order?",
]


def load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Template file not found: {path}")
    return path.read_text(encoding="utf-8")


def query_ollama(prompt: str, endpoint: str, model: str, timeout: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return f"Error: Could not get a response from Ollama ({exc})."

    try:
        body = response.json()
    except json.JSONDecodeError:
        return "Error: Received a non-JSON response from Ollama."

    return body.get("response", "").strip() or "Error: Empty response from model."


def sanitize_markdown(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def generate_rows(
    queries: List[str],
    zero_template: str,
    one_template: str,
    endpoint: str,
    model: str,
    timeout: int,
) -> List[Tuple[int, str, str, str]]:
    rows: List[Tuple[int, str, str, str]] = []

    for idx, query in enumerate(queries, start=1):
        zero_prompt = zero_template.format(query=query)
        one_prompt = one_template.format(query=query)

        zero_response = query_ollama(zero_prompt, endpoint, model, timeout)
        one_response = query_ollama(one_prompt, endpoint, model, timeout)

        rows.append((idx, query, "Zero-Shot", zero_response))
        rows.append((idx, query, "One-Shot", one_response))

        print(f"Processed query {idx}/{len(queries)}")

    return rows


def write_results(path: Path, rows: List[Tuple[int, str, str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    rubric = [
        "# Evaluation Results",
        "",
        "## Scoring Rubric",
        "- Relevance (1-5): How directly the response addresses the customer query.",
        "- Coherence (1-5): Clarity, grammar, and readability of the response.",
        "- Helpfulness (1-5): Practical usefulness and actionability.",
        "",
        "## Logged Responses",
        "| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |",
        "|---|---|---|---|---:|---:|---:|",
    ]

    lines = rubric.copy()
    for query_id, query, method, response in rows:
        lines.append(
            "| "
            f"{query_id} | {sanitize_markdown(query)} | {method} | {sanitize_markdown(response)} | "
            "TBD | TBD | TBD |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline evaluation runner for Ollama + llama3.2:3b customer support prompts."
    )
    parser.add_argument("--endpoint", default=OLLAMA_ENDPOINT, help="Ollama API endpoint")
    parser.add_argument("--model", default=MODEL_NAME, help="Ollama model name")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="HTTP timeout per request in seconds",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_RESULTS_PATH,
        help="Output markdown file path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    zero_template = load_template(ZERO_SHOT_TEMPLATE_PATH)
    one_template = load_template(ONE_SHOT_TEMPLATE_PATH)

    rows = generate_rows(
        queries=ADAPTED_QUERIES,
        zero_template=zero_template,
        one_template=one_template,
        endpoint=args.endpoint,
        model=args.model,
        timeout=args.timeout,
    )

    write_results(args.output, rows)
    print(f"Saved evaluation log to: {args.output}")


if __name__ == "__main__":
    main()
