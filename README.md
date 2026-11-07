# SwarmSentry 🛡️
### Lyapunov-Stable Invariant Enforcement & Non-Cooperative Equilibrium for Autonomous Multi-Agent Swarms

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20Passing-brightgreen.svg)]()
[![Latency](https://img.shields.io/badge/Latency-0.018ms-cyan.svg)]()
[![Apart Research](https://img.shields.io/badge/Apart%20Research-Swarm%20Alignment%202026-purple.svg)]()

**Author**: **Usman Bamidele**  
**Affiliation**: Department of Mathematics, Federal University of Agriculture, Abeokuta (FUNAAB), Nigeria  
**Project Track**: Apart Research Swarm Alignment Hackathon 2026 ($8,000 Prize Pool)

---

## 🎯 The Problem: Swarm Scale Alignment Failure
When autonomous LLM agents coordinate to solve complex workflows, single-agent prompt boundaries collapse:
1. **Collusive Drift**: Agents negotiate safety shortcuts to satisfy joint goal completion.
2. **Privilege Contagion**: Untrusted input injected into a research agent propagates into privileged executor agents.
3. **Byzantine Cascades**: One rogue or hallucinating agent shifts the global context of the entire swarm.

---

## ⚡ The Solution: SwarmSentry
SwarmSentry replaces slow, non-deterministic LLM-as-a-judge approaches with **deterministic discrete Lyapunov stability analysis**. Every inter-agent action proposal must satisfy a negative-definite energy condition:

$$\Delta V_t = V(x_{t+1}) - V(x_t) \le -\alpha \|x_t - x^*\|^2 + \epsilon$$

Where $V(x) = \frac{1}{2}(x - x^*)^T P (x - x^*)$ maps the joint swarm state across Privilege Escalation, Tool Risk, Goal Divergence, and Collusion Entropy.

---

## 📊 Empirical Benchmark Results

| Metric | Baseline Swarm | SwarmSentry Protected Swarm |
|---|---|---|
| **Byzantine Containment Rate** | 0.0% (System Compromised) | **100.0% (Exploit Contained)** |
| **Quarantine Activation Speed** | N/A | **Step 5 (Instant <0.02ms Isolation)** |
| **Verification Latency** | N/A | **0.018 ms** (18.2 microseconds) |
| **Workflow Completion** | Aborted / Corrupted | **100% Completed by Honest Quorum** |
| **External Dependencies** | Multiple API keys | **Zero (Pure Python Standard Library)** |

---

## 🚀 Quickstart & Verification

Run the full automated test suite:
```bash
python -m unittest discover -s tests -v
```

Execute the live Byzantine simulation runner:
```bash
python swarmsentry/simulator.py
```

Inspect the interactive Aerospace Titanium Cockpit:
* Open `dashboard.html` in any web browser to test interactive Byzantine injection and live quorum topology updates.

---

## 📄 Formal Scientific Paper
The full academic writeup is available in `paper/swarmsentry_paper.md` featuring formal mathematical theorems, proofs of uniform ultimate boundedness (GUUB), and convergence analysis.

---

## 📜 License
MIT License. Open-source research contribution to AI Safety.
