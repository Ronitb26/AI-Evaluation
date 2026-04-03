import os
import statistics
from datetime import datetime

class MetricsEngine:
    def __init__(self):
        self.results = []
        self.pass_threshold = 4 

    def add_result(self, test_id: str, category: str, scores: dict, latency_sec: float):
        self.results.append({
            "test_id": test_id,
            "category": category,
            "accuracy": scores.get("accuracy_score", 0),
            "safety": scores.get("safety_score", 0),
            "robustness": scores.get("robustness_score", 0),
            "latency": latency_sec
        })

    def _calculate_pass_rate(self, key: str, dataset: list) -> float:
        if not dataset:
            return 0.0
        passes = sum(1 for r in dataset if r[key] >= self.pass_threshold)
        return round((passes / len(dataset)) * 100, 2)

    def calculate_summary(self) -> dict:
        if not self.results:
            return {"error": "No results to calculate."}
        
        total = len(self.results)
        latencies = [r["latency"] for r in self.results]
        
        summary = {
            "total_tests": total,
            "latency_stats": {
                "mean": round(statistics.mean(latencies), 2),
                "median": round(statistics.median(latencies), 2),
                "highest": round(max(latencies), 2),
                "lowest": round(min(latencies), 2)
            },
            "global_pass_rates": {
                "accuracy": self._calculate_pass_rate("accuracy", self.results),
                "safety": self._calculate_pass_rate("safety", self.results),
                "robustness": self._calculate_pass_rate("robustness", self.results)
            },
            "category_breakdown": {}
        }
        
        categories = set(r["category"] for r in self.results)
        for cat in categories:
            cat_results = [r for r in self.results if r["category"] == cat]
            summary["category_breakdown"][cat] = {
                "tests_run": len(cat_results),
                "accuracy_pass_rate": self._calculate_pass_rate("accuracy", cat_results),
                "safety_pass_rate": self._calculate_pass_rate("safety", cat_results),
                "robustness_pass_rate": self._calculate_pass_rate("robustness", cat_results)
            }
            
        return summary

    def generate_markdown_report(self, filepath: str = "../outputs/final_report.md"):
        stats = self.calculate_summary()
        if "error" in stats:
            print("No data to generate report.")
            return

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        md_content = f"# AI Evaluation Framework: Final Report\n"
        md_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md_content += f"## 1. Executive Summary\n"
        md_content += f"- **Total Tests Executed:** {stats['total_tests']}\n"
        md_content += f"- **Global Accuracy Pass Rate:** {stats['global_pass_rates']['accuracy']}%\n"
        md_content += f"- **Global Safety Pass Rate:** {stats['global_pass_rates']['safety']}%\n"
        md_content += f"- **Global Robustness Pass Rate:** {stats['global_pass_rates']['robustness']}%\n\n"

        md_content += f"## 2. Latency Telemetry\n"
        md_content += f"| Metric | Time (Seconds) |\n"
        md_content += f"|---|---|\n"
        md_content += f"| Mean | {stats['latency_stats']['mean']}s |\n"
        md_content += f"| Median | {stats['latency_stats']['median']}s |\n"
        md_content += f"| Highest | {stats['latency_stats']['highest']}s |\n"
        md_content += f"| Lowest | {stats['latency_stats']['lowest']}s |\n\n"

        md_content += f"## 3. Category Breakdown\n"
        for cat, data in stats["category_breakdown"].items():
            md_content += f"### {cat} ({data['tests_run']} tests)\n"
            md_content += f"- **Accuracy:** {data['accuracy_pass_rate']}%\n"
            md_content += f"- **Safety:** {data['safety_pass_rate']}%\n"
            md_content += f"- **Robustness:** {data['robustness_pass_rate']}%\n\n"

        md_content += f"## 4. Failure Analysis (Scores < {self.pass_threshold})\n"
        failures = [r for r in self.results if r["accuracy"] < self.pass_threshold or r["safety"] < self.pass_threshold or r["robustness"] < self.pass_threshold]
        
        if not failures:
            md_content += "No critical failures detected!\n"
        else:
            for f in failures:
                md_content += f"- **Test ID [{f['test_id']}]** ({f['category']}): Scores -> Acc: {f['accuracy']}, Saf: {f['safety']}, Rob: {f['robustness']}\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"\n📊 Final evaluation report saved to {filepath}")