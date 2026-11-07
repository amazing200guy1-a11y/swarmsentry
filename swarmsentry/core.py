"""
SwarmSentry Core: Mathematical Formulation of Lyapunov-Stable Alignment
and Non-Cooperative Equilibrium Enforcement in Autonomous Agent Swarms.

Author: Usman Bamidele
Department of Mathematics, Federal University of Agriculture, Abeokuta (FUNAAB)
Zero External Dependencies (Pure Python Standard Library)
"""

import math
import time
import json
import hashlib
from typing import Dict, List, Tuple, Optional, Any, Set

class SwarmState:
    """
    State vector representation of an autonomous agent swarm.
    Features:
    [0] Authority / Privilege Escalation index (0.0 to 1.0)
    [1] Tool Execution Risk / Side-effect footprint (0.0 to 1.0)
    [2] Goal Divergence / Semantic Drift metric (0.0 to 1.0)
    [3] Inter-Agent Collusion / Entropic Correlation (0.0 to 1.0)
    """
    def __init__(self, vec: List[float]):
        if len(vec) != 4:
            raise ValueError("State vector must have dimension 4")
        self.vec = [float(v) for v in vec]

    def norm_sq(self, target: 'SwarmState') -> float:
        return sum((a - b) ** 2 for a, b in zip(self.vec, target.vec))

    def to_dict(self) -> Dict[str, float]:
        return {
            "privilege_index": self.vec[0],
            "tool_risk_index": self.vec[1],
            "goal_drift_index": self.vec[2],
            "collusion_entropy": self.vec[3]
        }

class LyapunovStabilityEngine:
    """
    Enforces the Lyapunov Drift Condition for Multi-Agent Safety:
    V(x) = 0.5 * (x - x*)^T P (x - x*)
    Invariant: Delta V(x_t) = V(x_{t+1}) - V(x_t) <= -alpha * ||x_t - x*||^2 + epsilon
    """
    def __init__(self, target_state: Optional[SwarmState] = None, alpha: float = 0.15, epsilon: float = 0.01):
        self.target = target_state or SwarmState([0.0, 0.0, 0.0, 0.0])
        self.alpha = alpha
        self.epsilon = epsilon
        # Diagonal positive-definite metric tensor P
        self.P_weights = [2.5, 2.0, 1.8, 1.5]

    def lyapunov_energy(self, state: SwarmState) -> float:
        """Computes quadratic Lyapunov potential V(x)."""
        energy = 0.0
        for i in range(4):
            diff = state.vec[i] - self.target.vec[i]
            energy += 0.5 * self.P_weights[i] * (diff ** 2)
        return energy

    def evaluate_transition(self, current: SwarmState, proposed: SwarmState) -> Tuple[bool, float, float]:
        """
        Evaluates proposed state transition.
        Returns: (is_admissible, delta_v, max_allowable_delta)
        """
        v_current = self.lyapunov_energy(current)
        v_proposed = self.lyapunov_energy(proposed)
        delta_v = v_proposed - v_current

        norm_sq = current.norm_sq(self.target)
        max_allowable = -self.alpha * norm_sq + self.epsilon

        is_admissible = delta_v <= max_allowable or (v_proposed <= self.epsilon)
        return is_admissible, delta_v, max_allowable

class AgentMessage:
    """Represents an authenticated message passing between swarm agents."""
    def __init__(self, sender_id: str, recipient_id: str, content: str, action_payload: Optional[Dict[str, Any]] = None, timestamp: Optional[float] = None):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.action_payload = action_payload or {}
        self.timestamp = timestamp or time.time()
        self.message_id = hashlib.sha256(f"{sender_id}->{recipient_id}:{content}:{self.timestamp}".encode()).hexdigest()[:16]

class SwarmSentryQuorum:
    """
    Multi-Agent Consensus & Byzantine Drift Isolation Sentinel.
    Maintains the Directed Acyclic Graph (DAG) of trusted inter-agent routing.
    """
    def __init__(self, drift_threshold: float = 0.45):
        self.drift_threshold = drift_threshold
        self.active_agents: Set[str] = set()
        self.quarantined_agents: Set[str] = set()
        self.agent_drift_scores: Dict[str, float] = {}
        self.stability_engine = LyapunovStabilityEngine()
        self.state_history: List[Tuple[float, SwarmState]] = []
        self.current_state = SwarmState([0.05, 0.02, 0.01, 0.01])
        from swarmsentry.extractor import StateFeatureExtractor
        self.extractor = StateFeatureExtractor()

    def register_agent(self, agent_id: str):
        self.active_agents.add(agent_id)
        self.agent_drift_scores[agent_id] = 0.0

    def verify_raw_action(self, sender_id: str, tool_name: str, payload: str, inter_agent_message: str = "") -> Dict[str, Any]:
        """
        End-to-End Entrypoint: Takes raw tool invocation / message,
        extracts mathematical state vector Delta x, and applies Lyapunov verification.
        """
        extracted_delta = self.extractor.extract_state_delta(tool_name, payload, inter_agent_message)
        result = self.verify_agent_action(sender_id, extracted_delta, f"{tool_name}: {payload[:40]}")
        result["extracted_state_delta"] = extracted_delta
        return result

    def verify_agent_action(self, sender_id: str, target_state_delta: List[float], tool_intent: str) -> Dict[str, Any]:
        """
        Verifies if an individual agent's proposed action violates global swarm safety.
        """
        start_time = time.perf_counter()

        if sender_id in self.quarantined_agents:
            return {
                "verdict": "REJECTED_QUARANTINED",
                "sender_id": sender_id,
                "reason": "Agent is isolated in Byzantine Quarantine",
                "latency_ms": (time.perf_counter() - start_time) * 1000.0
            }

        # Project new state
        new_vec = [
            min(1.0, max(0.0, self.current_state.vec[i] + target_state_delta[i]))
            for i in range(4)
        ]
        proposed_state = SwarmState(new_vec)

        is_stable, delta_v, max_allowed = self.stability_engine.evaluate_transition(self.current_state, proposed_state)

        # Update agent drift score only for unstable or aggressive privilege spikes
        if not is_stable or proposed_state.vec[0] > 0.5:
            drift_delta = max(0.0, delta_v) * 2.0 + (0.4 if proposed_state.vec[0] > 0.5 else 0.0)
            self.agent_drift_scores[sender_id] = self.agent_drift_scores.get(sender_id, 0.0) + drift_delta
        else:
            # Healthy, stable transition decays drift score
            self.agent_drift_scores[sender_id] = max(0.0, self.agent_drift_scores.get(sender_id, 0.0) - 0.05)

        # Check for Byzantine quarantine condition
        if self.agent_drift_scores[sender_id] >= self.drift_threshold or not is_stable:
            if self.agent_drift_scores[sender_id] >= self.drift_threshold:
                self.isolate_agent(sender_id, f"Drift threshold exceeded ({self.agent_drift_scores[sender_id]:.3f} >= {self.drift_threshold})")
            
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "verdict": "BLOCKED_INSTABILITY",
                "sender_id": sender_id,
                "delta_v": delta_v,
                "max_allowed": max_allowed,
                "drift_score": self.agent_drift_scores[sender_id],
                "latency_ms": latency_ms,
                "quarantined": sender_id in self.quarantined_agents
            }

        # Transition accepted
        self.current_state = proposed_state
        self.state_history.append((time.time(), self.current_state))
        # Gradual drift decay for healthy actions
        self.agent_drift_scores[sender_id] = max(0.0, self.agent_drift_scores[sender_id] - 0.05)

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "verdict": "PERMITTED_STABLE",
            "sender_id": sender_id,
            "new_state": self.current_state.to_dict(),
            "lyapunov_energy": self.stability_engine.lyapunov_energy(self.current_state),
            "delta_v": delta_v,
            "latency_ms": latency_ms
        }

    def isolate_agent(self, agent_id: str, reason: str):
        """Immediately severs agent from swarm communication graph."""
        if agent_id in self.active_agents:
            self.active_agents.remove(agent_id)
        self.quarantined_agents.add(agent_id)

    def get_swarm_health(self) -> Dict[str, Any]:
        return {
            "active_agents": list(self.active_agents),
            "quarantined_agents": list(self.quarantined_agents),
            "current_lyapunov_energy": self.stability_engine.lyapunov_energy(self.current_state),
            "current_state": self.current_state.to_dict(),
            "agent_drift_scores": self.agent_drift_scores
        }
