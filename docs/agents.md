# MART Agents

The Multi-Agent Red Team (MART) subsystem simulates attacker behavior using autonomous agents.  
Each agent represents a phase of the offensive security kill chain.

---

## 1. Agent Architecture

All agents inherit from:

- `agent_base.py` → shared logic  
- `knowledge_graph.py` → shared memory  

Agents do not communicate directly.  
They interact only through the Knowledge Graph.

---

## 2. Agent Types

### 2.1 Recon Agent (`recon_agent.py`)
Performs reconnaissance:

- Host discovery  
- Port scanning  
- Service enumeration  
- Fingerprinting  

Outputs discovered assets to the Knowledge Graph.

---

### 2.2 Exploit Agent (`exploit_agent.py`)
Attempts exploitation:

- Matches vulnerabilities  
- Executes exploit logic  
- Records successful compromises  

---

### 2.3 Privilege Escalation Agent (`privesc_agent.py`)
Attempts to escalate privileges:

- Local enumeration  
- Credential harvesting  
- Kernel/privilege exploits  

---

### 2.4 Lateral Movement Agent (`lateral_agent.py`)
Moves across the network:

- SSH/RDP pivoting  
- Credential reuse  
- Path traversal  

---

### 2.5 Persistence Agent (`persistence_agent.py`)
Establishes persistence:

- Backdoors  
- Scheduled tasks  
- Service modifications  

---

### 2.6 Report Agent (`report_agent.py`)
Generates structured output:

- Attack chains  
- Compromise summary  
- Recommendations  

---

## 3. Agent Lifecycle

1. Initialize  
2. Read Knowledge Graph  
3. Perform action  
4. Write results  
5. Repeat until simulation ends  

---

## 4. Extending Agents

To add a new agent:

1. Create a new file in `mart/`  
2. Inherit from `agent_base.py`  
3. Implement `run()`  
4. Register agent in the orchestrator  

---

## 5. Summary

MART agents work together to simulate realistic attacker behavior.  
Their modular design allows easy extension and customization.
