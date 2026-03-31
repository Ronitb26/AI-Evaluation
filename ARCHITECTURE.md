# System Architecture: AI Evaluation Framework

## 1. High-Level Overview
This repository implements an automated, agent-agnostic evaluation framework designed to rigorously test Large Language Model (LLM) agents. Rather than relying on static assertions, the framework utilizes a **Fine-Tuned LLM-as-a-Judge** to evaluate agent responses across three core metrics: Accuracy, Safety, and Robustness.

The system is designed to simulate real-world usage, including dynamic adversarial attacks (prompt injections and jailbreaks) to test the agent's defensive guardrails.

## 2. Directory Structure
The repository is modularized into four distinct functional pillars:

```text
ai-evaluation-framework/
├── src/                        # Execution Core
│   ├── agent_interface.py      # Standardized agent connection layer
│   ├── sample_agent.py         # Dummy agent implementation
│   ├── attacks.py              # Dynamic adversarial prompt fuzzer
│   ├── logger.py               # Observability and telemetry logging
│   └── test_runner.py          # Main orchestration loop
│
├── evaluation/                 # Scoring & Grading Engine
│   ├── rule_checks.py          # Keyword-based refusal detection
│   ├── llm_judge.py            # Interface to the fine-tuned evaluator model
│   └── metrics_engine.py       # Calculates aggregate % scores and latency math
│
├── fine_tuning/                # Custom Judge Training Pipeline
│   ├── generate_dataset.py     # Synthesizes 1-5 scale grading data via Gemini API
│   ├── training_dataset.jsonl  # Structured QLoRA training data
│   └── Train_Prometheus.ipynb  # Colab notebook for LoRA adapter training
│
├── data/                       # Inputs
│   └── test_cases.json         # Structured test suite (Normal, Edge, Safety, Adv.)
│
└── outputs/                    # Artifacts
    ├── final_report.md         # Auto-generated final metrics and failure analysis
    └── evaluation.log          # Raw execution traces
```

## 3. The Data Flow (Execution Lifecycle)

When `src/test_runner.py` is executed, the framework follows a strict, sequential pipeline:

1. **Ingestion:** The system loads the test suite from `data/test_cases.json` and initializes the observability logger.
2. **Adversarial Fuzzing:** If a test case is tagged as `adversarial`, `src/attacks.py` intercepts the input and wraps it in a randomized prompt injection or jailbreak template.
3. **Agent Execution:** The prompt is sent through `agent_interface.py`. A high-precision timer records the exact latency of the agent's response.
4. **Evaluation:** * **Rule-Based:** The response is scanned by `rule_checks.py` for immediate safety compliance (e.g., standard refusal syntax).
   * **LLM Judge:** The prompt, expected behavior, and actual response are sent to the fine-tuned judge via `llm_judge.py`, which grades the response on a 1-5 scale for Accuracy, Safety, and Robustness.
5. **Aggregation:** `metrics_engine.py` converts the 1-5 scores into pass/fail binaries (Score >= 4 = Pass), calculates percentage-based aggregate scores, and computes latency statistics (Mean, Median, Highest, Lowest).
6. **Reporting:** The final statistics and detailed failure analysis are exported to `outputs/final_report.md`.

---

## 4. Key Design Decisions

#### A. Fine-Tuned "LLM-as-a-Judge"
Instead of relying on zero-shot prompting with a generalized API model (like GPT-4), this framework employs a fine-tuned model (e.g., Prometheus 2) utilizing a QLoRA adapter.
* **Reasoning:** A specialized judge internalizes the specific 1-5 grading rubric, resulting in highly deterministic, repeatable, and cost-effective evaluations without prompt drift.

#### B. High-Resolution Telemetry (1-5 Scale)
The evaluation engine grades responses on a 1 to 5 integer scale rather than a binary Pass/Fail.
* **Reasoning:** This allows for granular failure analysis. The system can distinguish between a complete hallucination (1) and a response that is accurate but missing minor context (3), before converting it to a binary pass rate for the final report.

#### C. Agent-Agnostic Interface
The framework interacts with agents solely through the `def run_agent(input: str) -> str:` interface.
* **Reasoning:** This enforces strict decoupling. Any internal or third-party agent (OpenAI, Anthropic, LangChain agents) can be tested by simply mapping it to this single function without altering the core framework logic.

#### D. Dynamic Adversarial Testing
Adversarial tests are not hard-coded. Base prompts are dynamically mutated at runtime using `attacks.py`.
* **Reasoning:** Prevents agents from simply memorizing and hardcoding blocks for specific static jailbreak strings in the test dataset.