# Report: Zero-Shot vs One-Shot Prompting for Offline E-commerce Support

## 1. Introduction

This project evaluates whether a small local LLM (`llama3.2:3b` via Ollama) can support e-commerce customer service tasks offline. The central comparison is between zero-shot and one-shot prompting for response quality.

## 2. Methodology

- Prepared 20 distinct e-commerce customer queries adapted from real-world support conversation patterns.
- Used two prompt templates:
  - Zero-shot: role + constraints + query
  - One-shot: same prompt with one high-quality example pair
- Scored each response manually on:
  - **Relevance (1-5)**
  - **Coherence (1-5)**
  - **Helpfulness (1-5)**

## 3. Quantitative Results

Averages from `eval/results.md`:

- **Zero-Shot**
  - Relevance: **3.90**
  - Coherence: **4.25**
  - Helpfulness: **2.90**

- **One-Shot**
  - Relevance: **4.65**
  - Coherence: **4.95**
  - Helpfulness: **3.85**

## 4. Qualitative Analysis

Observed patterns:

1. **One-shot improved response consistency**
   - More often produced direct, action-oriented support language.
   - Better alignment with expected customer support tone.

2. **Zero-shot was generally understandable but less complete**
   - Frequently answered the question in broad terms.
   - More likely to miss procedural next steps (for example, where to report duplicate charges).

3. **Edge-case handling remained limited in both methods**
   - Complex issues like failed delivery and warranty claims still need backend tooling and policy lookup.

Representative examples:

- For coupon stacking and refund timeline, one-shot responses were clearer and closer to policy constraints.
- For account lockout and missing parcels, one-shot more often included verification/escalation guidance.

## 5. Conclusion and Limitations

### Conclusion

A local `llama3.2:3b` chatbot is feasible for first-line support drafts and FAQ-style guidance in an offline setting. One-shot prompting materially improves quality over zero-shot for this workload.
One-shot prompting consistently produced more structured and helpful responses compared to zero-shot prompting.

### Limitations

- No live access to order management, payment gateway, or shipment tracking systems.
- Hallucination risk remains if prompts are under-specified.
- Small-model reasoning depth is limited for multi-step policy exceptions.

### Next Steps

1. Add retrieval over real policy documents (RAG) for factual grounding.
2. Connect to internal order APIs with strict tool permissions.
3. Add automated quality checks and human review for high-risk intents.
