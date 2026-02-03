# Predictors

Predictors in AAPP‑MART provide the decision‑making and inference capabilities that support agents and pipelines.  
They analyze input data, generate predictions, evaluate conditions, and guide autonomous behavior.  
This document explains the predictor architecture, available predictor types, and how to build custom models.

---

## Predictor Architecture

All predictors inherit from the base class:

```
aapp-mart/predictors/base_predictor.py
```

A typical predictor implements:

- `load()` — loads model resources  
- `predict(input_data)` — performs inference  
- `validate(input_data)` — optional input validation  
- `info()` — metadata about the predictor  

Predictors are stateless by default, but can maintain internal state if needed.

---

## Predictor Types

AAPP‑MART includes three primary predictor categories:

---

## 1. Machine Learning Predictors

Located in:

```
aapp-mart/predictors/ml_predictor.py
```

Machine learning predictors use statistical or learned models to generate predictions.

Typical use cases:

- Anomaly detection  
- Classification  
- Regression  
- Behavioral prediction  
- Risk scoring  

Example structure:

```python
class MLPredictor(BasePredictor):
    def load(self):
        pass

    def predict(self, data):
        return {"score": 0.87}
```

---

## 2. Rule‑Based Predictors

Located in:

```
aapp-mart/predictors/rule_predictor.py
```

Rule‑based predictors use deterministic logic instead of learned models.

Common use cases:

- Threshold checks  
- Conditional logic  
- Pattern matching  
- Static decision trees  

Example:

```python
class RulePredictor(BasePredictor):
    def predict(self, data):
        if data.get("cpu") > 90:
            return {"alert": "high_cpu"}
        return {"alert": "normal"}
```

Rule‑based predictors are fast, transparent, and easy to debug.

---

## 3. Hybrid Predictors

Located in:

```
aapp-mart/predictors/hybrid_predictor.py
```

Hybrid predictors combine ML models with rule‑based logic.

Use cases:

- ML prediction + rule validation  
- Multi‑stage decision pipelines  
- Confidence‑based fallback logic  

Example workflow:

1. ML model generates a probability score  
2. Rule engine validates or adjusts the output  
3. Final decision returned to the orchestrator  

Hybrid predictors offer the best balance between accuracy and interpretability.

---

## Using Predictors in Pipelines

Predictors are commonly used inside pipelines:

```python
from aappmart.predictors.ml_predictor import MLPredictor

predictor = MLPredictor()
predictor.load()

result = predictor.predict({"input": "data"})
```

Pipelines can chain multiple predictors:

```python
pipeline = ["SystemAgent", "MLPredictor", "RulePredictor"]
```

---

## Creating a Custom Predictor

To create your own predictor:

1. Create a new file under `src/aapp-mart/predictors/`
2. Inherit from `BasePredictor`
3. Implement the required methods

Example:

```python
class CustomPredictor(BasePredictor):
    def load(self):
        pass

    def predict(self, data):
        return {"custom_output": True}
```

---

## Best Practices

- Keep predictors modular and stateless  
- Validate input before inference  
- Return structured outputs (dict or dataclass)  
- Use logging instead of print statements  
- Avoid heavy dependencies unless necessary  
- Document expected input and output formats  

---

## Future Extensions

Planned enhancements include:

- Deep learning predictor support  
- Online learning models  
- Predictor registry with auto‑discovery  
- GPU‑accelerated inference  
- Distributed prediction pipelines  

---

Predictors form the intelligence layer of AAPP‑MART, enabling agents and pipelines to make informed, autonomous decisions.  
As the framework evolves, additional predictor types and advanced inference engines will be introduced.
