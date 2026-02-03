# Modules

AAPP‑MART modules provide specialized capabilities that agents can use to perform system analysis, network operations, memory inspection, automation tasks, and controlled testing.  
Modules are designed to be lightweight, isolated, and easily extendable, allowing developers to plug in new functionality without modifying the core framework.

---

## Module Architecture

Each module follows a simple and consistent structure:

- A dedicated directory under `src/aapp-mart/modules/`
- An `__init__.py` file to define the module package
- One or more Python files implementing module functionality
- Optional helper utilities or configuration files

Modules are invoked by agents or pipelines and can return structured results back to the orchestrator.

---

## Module Categories

AAPP‑MART includes five primary module categories:

### 1. System Modules
Located in:

```
aapp-mart/modules/system/
```

System modules provide access to operating system information and local machine resources.

Typical capabilities include:

- System information collection  
- Process enumeration  
- Disk and memory statistics  
- OS metadata extraction  

Example file: `system_info.py`

---

### 2. Network Modules
Located in:

```
aapp-mart/modules/network/
```

Network modules enable agents to perform network‑related operations.

Common features:

- Network scanning  
- Port enumeration  
- Connection mapping  
- Basic protocol inspection  

Example file: `network_scan.py`

---

### 3. Memory Modules
Located in:

```
aapp-mart/modules/memory/
```

Memory modules focus on memory inspection and analysis.

Possible functionality:

- Memory dump parsing  
- Pattern searching  
- Lightweight forensic extraction  

Example file: `memory_parser.py`

---

### 4. Automation Modules
Located in:

```
aapp-mart/modules/automation/
```

Automation modules allow agents to perform automated tasks and workflows.

Typical use cases:

- Task scheduling  
- Script execution  
- Automated system actions  
- Workflow orchestration  

Example file: `task_automation.py`

---

### 5. Offensive Modules
Located in:

```
aapp-mart/modules/offensive/
```

Offensive modules are reserved for **controlled, ethical testing scenarios** such as simulation environments or sandboxed research.  
These modules are intentionally minimal by default and should be used responsibly.

Example file: `placeholder.py`

---

## Using Modules in Agents

Agents can import and use modules directly:

```python
from aappmart.modules.system.system_info import SystemInfo

class SystemAgent(BaseAgent):
    def run(self):
        info = SystemInfo().collect()
        return info
```

Modules are designed to be stateless and reusable across multiple agents.

---

## Creating a Custom Module

To create a new module:

1. Add a new directory under `aappmart/modules/`
2. Include an `__init__.py` file
3. Implement your module logic in a Python file
4. Optionally register it for discovery

Example structure:

```
aapp-mart/modules/custom_module/
    ├── __init__.py
    └── custom_tool.py
```

---

## Best Practices

- Keep modules focused on a single responsibility  
- Avoid heavy dependencies unless necessary  
- Return structured data (dict or dataclass)  
- Ensure modules do not modify global state  
- Use logging instead of print statements  

---

AAPP‑MART’s modular design allows developers to expand the framework with new capabilities quickly and safely.  
As the project evolves, additional module categories and advanced tooling will be introduced.
