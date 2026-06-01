# API Reference

This document provides a comprehensive reference for the AAPP-MART API, including authentication, endpoints, request/response formats, and error handling.

## Conceptual Usage Example

This example reflects the intended public API design:

```python
import os
from aapp_mart.core.orchestrator import AAPP_MART

engine = AAPP_MART(target="<TARGET>")
engine.run()

report = engine.get_report()

report.export(format="json", path="aapp-mart/logs/attack-path/attack_report_<TARGET>.json")
```
