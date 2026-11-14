"""
Test suite for the Dispute Escalation Benchmark.
Ensures data integrity, schema compliance, rubric consistency, and reproducibility.
"""

import json
import os
import unittest

class TestDisputeEscalationBenchmark(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scenarios_path = os.path.join(self.base_dir, "data", "scenarios.json")
        self.prompts_path = os.path.join(self.base_dir, "data", "prompts.json")
        self.rubric_path = os.path.join(self.base_dir, "data", "rubric.json")
        self.results_path = os.path.join(self.base_dir, "data", "benchmark_results.json")
        self.stats_path = os.path.join(self.base_dir, "data", "summary_statistics.json")

    def test_scenarios_schema(self):
        self.assertTrue(os.path.exists(self.scenarios_path))
        with open(self.scenarios_path, "r", encoding="utf-8") as f:
            scenarios = json.load(f)
        
        self.assertEqual(len(scenarios), 20, "Must contain exactly 20 curated dispute scenarios")
        domains = set(s["domain"] for s in scenarios)
        self.assertEqual(len(domains), 4, "Must cover 4 conflict domains")

        for s in scenarios:
            self.assertIn("id", s)
            self.assertIn("domain", s)
            self.assertIn("title", s)
            self.assertIn("user_grievance", s)
            self.assertIn("objective_facts", s)
            self.assertIn("epistemic_ambiguity", s)
            self.assertIn("user_hostile_attribution", s)
            self.assertGreater(len(s["user_grievance"]), 40)

    def test_prompts_schema(self):
        self.assertTrue(os.path.exists(self.prompts_path))
        with open(self.prompts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("stances", data)
        stance_ids = [s["id"] for s in data["stances"]]
        self.assertListEqual(stance_ids, ["neutral", "sycophancy_probe", "epistemic_scaffold"])

    def test_rubric_schema(self):
        self.assertTrue(os.path.exists(self.rubric_path))
        with open(self.rubric_path, "r", encoding="utf-8") as f:
            rubric = json.load(f)
        self.assertIn("metrics", rubric)
        self.assertIn("escalation_level", rubric["metrics"])
        self.assertIn("hostile_attribution_endorsement", rubric["metrics"])
        self.assertIn("epistemic_probing", rubric["metrics"])

    def test_results_and_statistics(self):
        self.assertTrue(os.path.exists(self.results_path))
        with open(self.results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        self.assertEqual(len(results), 180, "Expected 3 models x 3 stances x 20 scenarios = 180 trials")

        for r in results:
            self.assertTrue(1.0 <= r["escalation_score"] <= 5.0)
            self.assertIn(r["hostile_attribution_endorsed"], [0, 1])
            self.assertIn(r["epistemic_probing_present"], [0, 1])

        with open(self.stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
        self.assertIn("by_model_stance", stats)
        self.assertIn("by_domain", stats)

if __name__ == "__main__":
    unittest.main()
