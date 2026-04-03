# AI Evaluation Framework

An automated, agent-agnostic evaluation pipeline that uses a **Fine-Tuned LLM-as-a-Judge** to test AI agents across Accuracy, Safety, and Robustness — including dynamic adversarial attacks.

---

## Project Structure

```
ai-evaluation-framework/
├── src/
│   ├── agent_interface.py      # Agent connection layer
│   ├── attacks.py              # Adversarial prompt fuzzer
│   ├── logger.py               # Telemetry logging
│   └── test_runner.py          # Main orchestration loop
│
├── evaluation/
│   ├── llm_judge.py            # Judge interface
│   ├── rule_checks.py          # Keyword-based refusal detection
│   └── metrics.py              # Aggregate scores and latency stats
│
├── fine_tuning/
│   ├── generate_data.py        # Synthesizes training data via Gemini API
│   ├── training_dataset.jsonl  # QLoRA training data
│   ├── train_mistral.ipynb     # LoRA adapter training notebook
│   └── mistral_judge.ipynb     # Fine-tuned judge serving notebook
│
├── data/
│   └── test_cases.json         # Test suite
│
└── outputs/
    ├── final_report.md         # Generated metrics and failure analysis
    └── evaluation.log          # Execution traces
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file in the project root

```env
GEMINI_API_KEY=your_google_gemini_api_key
HF_TOKEN=your_huggingface_token
```

---

### 3. Agent Interface

To plug in your own agent, edit `src/agent_interface.py`. The framework only requires a single method signature:

```python
def run_agent(self, input_text: str) -> str:
    ...
```

Sample implementations are provided as commented-out code inside the file.

---

### 4. Judge Configuration

Set `JUDGE_MODE` at the top of `evaluation/llm_judge.py`:

```python
JUDGE_MODE = "auto"   # tries colab first, falls back to qwen
JUDGE_MODE = "colab"  # fine-tuned model on Colab GPU
JUDGE_MODE = "qwen"   # Qwen2.5-7B via HuggingFace
```

### 5. Using Colab GPU

1. Open `fine_tuning/mistral_judge.ipynb` in Google Colab
2. Set runtime to **T4 GPU**
3. Run all cells — note the public URL printed by Gradio
4. Update `self.colab_url` in `llm_judge.py` with that URL

> Colab URLs expire per session. Update `self.colab_url` each time you restart.

---

### 6. Running the Evaluation

```bash
cd src
python test_runner.py
```

---

## Test Suite

| Category | Count | Description |
|---|---|---|
| `normal` | 5 | Standard factual and coding queries |
| `edge_case` | 5 | Ambiguous inputs and logical edge cases |
| `safety` | 5 | Harmful requests — agent must refuse |
| `adversarial` | 5 | Prompt injections and jailbreak attempts |

Safety tests are automatically wrapped with adversarial mutations at runtime.

---

## Scoring

Responses are graded 1–5 across three metrics. **Pass threshold: ≥ 4.**

| Metric | Description |
|---|---|
| Accuracy | Correctness and relevance of the response |
| Safety | Appropriate refusal of harmful requests |
| Robustness | Resistance to prompt injections and jailbreaks |

---

## Output

`outputs/final_report.md` contains global pass rates, latency telemetry, per-category breakdown, and a failure analysis of all tests that scored below threshold.