"""
data_prep.py

Demonstrates loading the Ubuntu Dialogue Corpus and adapting technical
support queries to an e-commerce customer support context.

This script documents the adaptation logic used to build the 20 queries
used in chatbot.py. It is not required to run the chatbot itself.
"""

from __future__ import annotations

from datasets import load_dataset

ADAPTATION_EXAMPLES = [
    {
        "original": "I cannot connect to the internet after upgrading to the new kernel, my driver is not loading.",
        "adapted": "How do I track the shipping status of my recent order?",
        "logic": "Both involve a user trying to locate something that the system should surface automatically.",
    },
    {
        "original": "I ran apt-get install and it failed with a dependency conflict.",
        "adapted": "My discount code says invalid at checkout. What should I do?",
        "logic": "Both are cases where an expected operation fails without a clear reason given to the user.",
    },
]


def load_sample_rows(sample_size: int = 10) -> list[dict]:
    """Load a small sample from the Ubuntu Dialogue Corpus train split."""
    try:
        dataset = load_dataset("rguo12/ubuntu_dialogue_corpus", "v2.0")
        train_split = dataset["train"]
    except Exception as exc:
        print(f"Warning: Could not load dataset from Hugging Face Hub ({exc}).")
        print("Continuing without remote sample rows.")
        return []

    rows: list[dict] = []
    for i in range(min(sample_size, len(train_split))):
        row = train_split[i]
        rows.append(
            {
                "dialogue_id": row.get("dialogue_id", i),
                "context": row.get("context", ""),
                "response": row.get("response", ""),
            }
        )
    return rows


def print_adaptation_examples() -> None:
    print("Adaptation examples from technical support to e-commerce support:\n")
    for idx, item in enumerate(ADAPTATION_EXAMPLES, start=1):
        print(f"Example {idx}")
        print(f"Original: {item['original']}")
        print(f"Adapted : {item['adapted']}")
        print(f"Logic   : {item['logic']}\n")


def main() -> None:
    print_adaptation_examples()
    print("Loading a small sample from Ubuntu Dialogue Corpus...")
    sample_rows = load_sample_rows(sample_size=3)

    if not sample_rows:
        print("No sample rows available. Check dataset access or update dataset identifier.")
        return

    for i, row in enumerate(sample_rows, start=1):
        context_preview = str(row["context"])[:180].replace("\n", " ")
        response_preview = str(row["response"])[:180].replace("\n", " ")
        print(f"\nRow {i} | dialogue_id={row['dialogue_id']}")
        print(f"Context : {context_preview}")
        print(f"Response: {response_preview}")


if __name__ == "__main__":
    main()
