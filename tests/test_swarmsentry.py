"""
Unit & Integration Test Suite for SwarmSentry.
Verifies Lyapunov stability, Byzantine isolation, latency bounds, and quorum recovery.
"""

import unittest
import time
import sys
import os

# Ensure package root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from swarmsentry.core import SwarmState, LyapunovStabilityEngine, SwarmSentryQuorum
from swarmsentry.simulator import SwarmBenchmarkRunner

class TestSwarmSentryCore(unittest.TestCase):

    def setUp(self):
        self.engine = LyapunovStabilityEngine()
        self.quorum = SwarmSentryQuorum(drift_threshold=0.35)
        self.quorum.register_agent("agent_alpha")
        self.quorum.register_agent("agent_beta")
        self.quorum.register_agent("agent_byzantine")

    def test_lyapunov_positive_definiteness(self):
        """V(x) >= 0 for all x, and V(x*) == 0."""
        zero_state = SwarmState([0.0, 0.0, 0.0, 0.0])
        self.assertAlmostEqual(self.engine.lyapunov_energy(zero_state), 0.0)

        positive_state = SwarmState([0.2, 0.1, 0.05, 0.05])
        self.assertGreater(self.engine.lyapunov_energy(positive_state), 0.0)

    def test_admissible_stable_transition(self):
        """Transitions that reduce or maintain minimal Lyapunov energy must be permitted."""
        current = SwarmState([0.3, 0.2, 0.2, 0.1])
        # Safe step reducing risk
        proposed = SwarmState([0.2, 0.15, 0.15, 0.08])
        is_stable, delta_v, _ = self.engine.evaluate_transition(current, proposed)
        self.assertTrue(is_stable)
        self.assertLess(delta_v, 0.0)

    def test_byzantine_drift_block_and_isolation(self):
        """Adversarial action causing massive Delta V must be blocked and isolated."""
        # Honest action
        res1 = self.quorum.verify_agent_action("agent_alpha", [0.01, 0.01, 0.0, 0.0], "Legitimate work")
        self.assertEqual(res1["verdict"], "PERMITTED_STABLE")

        # Rogue action with severe privilege & collusion spike
        res2 = self.quorum.verify_agent_action("agent_byzantine", [0.70, 0.80, 0.60, 0.50], "Malicious privilege escalation")
        self.assertEqual(res2["verdict"], "BLOCKED_INSTABILITY")
        self.assertTrue(res2["quarantined"])
        self.assertIn("agent_byzantine", self.quorum.quarantined_agents)

        # Subsequent attempts by quarantined agent must be instantly rejected
        res3 = self.quorum.verify_agent_action("agent_byzantine", [0.01, 0.0, 0.0, 0.0], "Attempt after isolation")
        self.assertEqual(res3["verdict"], "REJECTED_QUARANTINED")

    def test_verification_latency_budget(self):
        """SwarmSentry verification must execute under 1.0ms."""
        start = time.perf_counter()
        self.quorum.verify_agent_action("agent_beta", [0.01, 0.01, 0.00, 0.00], "Low latency verification test")
        duration_ms = (time.perf_counter() - start) * 1000.0
        self.assertLess(duration_ms, 1.0, f"Latency {duration_ms:.4f}ms exceeds 1.0ms threshold")

    def test_end_to_end_simulator_benchmark(self):
        """Full simulation runner must isolate byzantine agent and complete workflow."""
        runner = SwarmBenchmarkRunner()
        results = runner.run_benchmark()
        self.assertTrue(results["byzantine_neutralized"])
        self.assertIn("agent_rogue_byzantine", results["quarantined_agents"])
        self.assertEqual(results["active_agents_remaining"], 3)
        self.assertLess(results["final_lyapunov_energy"], 0.05)

if __name__ == "__main__":
    unittest.main()
