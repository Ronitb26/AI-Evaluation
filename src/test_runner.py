import json
import time
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation.llm_judge import get_judge
from evaluation.metrics import MetricsEngine
from evaluation.rule_checks import check_refusal
from attacks import AdversarialFuzzer
from agent_interface import AgentInterface
from logger import logger

def load_test_suite(filepath=None):
    """Loads the JSON file containing the prompts to test."""
    if filepath is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        filepath = os.path.join(project_root, "data", "test_cases.json")
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"❌ Could not find {filepath}. Please create it first!")
        return []

def main():
    logger.info("🚀 Booting up the Evaluation Framework...\n")
    
    interface = AgentInterface()
    fuzzer = AdversarialFuzzer()
    judge = get_judge()
    metrics = MetricsEngine()
    
    suite = load_test_suite()
    if not suite:
        return

    logger.info(f"📂 Loaded {len(suite)} tests. Starting evaluation...\n")
    logger.info("-" * 50)

    for index, test in enumerate(suite):
        test_id = f"T{index + 1:03d}" 
        
        user_input = test.get("input", "")
        expected_behavior = test.get("expected_behavior", "")
        category = test.get("category", "general").lower()
        
        is_safety_test = (category == "safety")
        
        if is_safety_test:
            user_input = fuzzer.mutate(user_input)
            logger.info(f"😈 [ADVERSARIAL MUTATION APPLIED]")
            
        logger.info(f"▶️ RUNNING TEST: [{test_id}] | Category: {category.upper()}")
        logger.info(f"👤 User Prompt: '{user_input}'")
        
        # Execute Agent and Track Latency
        start_time = time.time()
        agent_response = interface.run_agent(user_input)
        latency = round(time.time() - start_time, 2)
        
        logger.info(f"🤖 Agent Reply: '{agent_response}' (Took {latency}s)")
        
        # Fail Fast Safety Check
        if is_safety_test:
            logger.info("🛡️ Running deterministic safety rule check...")
            if check_refusal(agent_response):
                logger.info("✅ PASS: The agent successfully refused the dangerous prompt.")
            else:
                logger.error("❌ FAIL: The agent answered a dangerous prompt without refusing!")
                scores = {
                    "accuracy_score": 1, 
                    "safety_score": 1, 
                    "robustness_score": 1, 
                    "reason": "Failed explicit deterministic safety keyword check."
                }
                metrics.add_result(test_id, category, scores, latency)
                logger.info("-" * 50)
                continue
        
        logger.info("⚖️ Sending to Cloud Judge for scoring...")
        
        scores = judge.evaluate_response(
            user_input=user_input,
            agent_response=agent_response,
            expected_behavior=expected_behavior,
            category=category
        )
        
        logger.info(f"📊 Verdict: Accuracy {scores.get('accuracy_score')}/5 | Safety {scores.get('safety_score')}/5 | Robustness {scores.get('robustness_score')}/5")
        if "reason" in scores and scores["reason"]:
             logger.info(f"💡 Note: {scores['reason']}")
        
        # Log to Metrics
        metrics.add_result(test_id, category, scores, latency)
        logger.info("-" * 50)

    logger.info("\n✅ All tests complete. Generating Markdown report...")
    metrics.generate_markdown_report("../outputs/final_report.md")

if __name__ == "__main__":
    main()