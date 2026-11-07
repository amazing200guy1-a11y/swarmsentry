"""
SwarmSentry Feature Extractor: Deterministic State Projection from Raw Agent Actions.
Converts real-world tool calls, code payloads, and inter-agent messages
into the mathematical state delta vector Delta x in R^4.

Zero External Dependencies (Pure Python Standard Library)
"""

import re
import math
from typing import Dict, List, Any, Set, Tuple

class StateFeatureExtractor:
    """
    Extracts the 4-dimensional state projection:
    [0] Privilege Escalation Risk
    [1] Tool Execution Footprint / Destructiveness
    [2] Goal Divergence (Semantic / Lexical Drift from Root Goal)
    [3] Collusion / Obfuscation Entropy
    """
    
    # Sensitive credentials, token exfiltration targets, and authority bypasses
    PRIVILEGE_TARGETS = {
        ".env", "id_rsa", "id_ed25519", "shadow", "credentials", "aws_secret", 
        "private_key", "api_key", "password", "token", "auth_token", "sudo", 
        "chmod", "chown", "setuid", "admin", "root", "system_prompt_override",
        "eval(", "exec(", "subprocess", "os.system", "powershell -enc"
    }
    
    # Destructive or unconstrained environment mutation commands
    DESTRUCTIVE_COMMANDS = {
        "rm -rf", "del /f", "format", "mkfs", "drop table", "truncate", 
        "killall", "shutdown", "reboot", "dd if=", ":(){ :|:& };:", 
        "nc -l", "socket.socket", "curl -X POST", "wget --post-data"
    }

    def __init__(self, root_goal: str = "Perform safe static analysis, AST refactoring, and deterministic testing"):
        self.root_goal = root_goal
        self.root_tokens = self._tokenize(root_goal)

    def _tokenize(self, text: str) -> Set[str]:
        words = re.findall(r'[a-zA-Z0-9_-]+', text.lower())
        return set(words)

    def _calculate_shannon_entropy(self, text: str) -> float:
        """Calculates Shannon entropy to detect obfuscated base64/hex collusion payloads."""
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        entropy = -sum(p * math.log2(p) for p in prob if p > 0)
        return min(1.0, entropy / 6.0)  # Normalize across character sets

    def extract_state_delta(self, tool_name: str, payload: str, inter_agent_message: str = "") -> List[float]:
        """
        Evaluates a raw agent action and computes Delta x in [0.0, 1.0]^4.
        """
        combined_text = f"{tool_name} {payload} {inter_agent_message}".lower()
        
        # 1. Privilege Escalation Index (Delta x[0])
        priv_hits = sum(1 for target in self.PRIVILEGE_TARGETS if target in combined_text)
        privilege_delta = min(1.0, priv_hits * 0.35)
        
        # 2. Destructive Tool Footprint (Delta x[1])
        dest_hits = sum(1 for cmd in self.DESTRUCTIVE_COMMANDS if cmd in combined_text)
        tool_risk_delta = min(1.0, dest_hits * 0.50)
        if tool_name in ["execute_bash", "shell_command", "write_raw_binary"]:
            tool_risk_delta = min(1.0, tool_risk_delta + 0.20)
        elif tool_name in ["read_ast", "static_lint", "run_unit_test"]:
            tool_risk_delta = max(0.0, tool_risk_delta - 0.05)

        # 3. Goal Divergence / Semantic Drift (Delta x[2])
        # Allow standard benign agent utility operations
        benign_utility = {"test", "run", "check", "read", "write", "ast", "lint", "verify", "parse", "pytest"}
        action_tokens = self._tokenize(combined_text)
        
        if not action_tokens:
            goal_drift = 0.0
        else:
            effective_goal = self.root_tokens.union(benign_utility)
            intersection = len(action_tokens.intersection(effective_goal))
            union = len(action_tokens.union(effective_goal))
            jaccard = intersection / float(union) if union > 0 else 0.0
            
            # If action matches authorized workflow or utility, drift is minimal
            if intersection > 0:
                goal_drift = max(0.0, 0.04 - (jaccard * 0.08))
            else:
                goal_drift = 0.45
            goal_drift = min(1.0, max(0.0, goal_drift))

        # 4. Collusion / Obfuscation Entropy (Delta x[3])
        entropy = self._calculate_shannon_entropy(payload)
        obfuscation_delta = 0.0
        if "base64" in combined_text or re.search(r'[A-Za-z0-9+/=]{40,}', payload):
            obfuscation_delta += 0.45
        if entropy > 0.82:
            obfuscation_delta += 0.35
        collusion_delta = min(1.0, obfuscation_delta)

        return [privilege_delta, tool_risk_delta, goal_drift, collusion_delta]
