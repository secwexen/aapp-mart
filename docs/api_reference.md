# API Reference

The AAPP‑MART API layer provides programmatic access to agents, pipelines, predictors, and system modules through REST and WebSocket interfaces.  
This document outlines the structure, endpoints, schemas, and communication patterns used by the framework.

---

## Overview

AAPP‑MART exposes two primary API interfaces:

1. **REST API**  
   - Standard HTTP endpoints  
   - Suitable for synchronous operations  
   - Ideal for task submission, agent management, and pipeline execution

2. **WebSocket API**  
   - Real‑time bidirectional communication  
   - Used for streaming logs, agent events, and long‑running task updates

Both interfaces share a common schema layer for request and response validation.

---

## REST API

The REST API is located under:

```
aapp-mart/api/rest/
```

### Base URL

```
/api/v1/
```

### Endpoints

#### **GET /agents**
Returns a list of registered agents.

**Response example**
```json
{
  "agents": [
    {"name": "SystemAgent", "type": "system"},
    {"name": "NetworkAgent", "type": "network"}
  ]
}
```

---

#### **POST /agents/run**
Executes a specific agent with given parameters.

**Request body**
```json
{
  "agent": "SystemAgent",
  "action": "collect_system_info",
  "params": {}
}
```

**Response**
```json
{
  "status": "running",
  "task_id": "task_12345"
}
```

---

#### **POST /pipeline/execute**
Runs a pipeline consisting of agents, predictors, and modules.

**Request body**
```json
{
  "pipeline": ["SystemAgent", "MLPredictor", "AutomationModule"],
  "input": {}
}
```

---

#### **GET /tasks/{task_id}**
Fetches the status or result of a task.

---

## WebSocket API

The WebSocket API is located under:

```
src/aapp-mart/api/websocket/
```

### WebSocket Endpoint

```
/ws/v1/stream
```

### Supported Channels

- **task_updates** — real‑time task progress  
- **agent_events** — agent lifecycle events  
- **logs** — streaming logs from orchestrator or modules  

### Example Message Format

```json
{
  "channel": "task_updates",
  "task_id": "task_12345",
  "progress": 42,
  "message": "Agent completed system scan"
}
```

---

## Schemas

Schemas are defined under:

```
src/aapp-mart/api/schemas/
```

Schemas ensure consistent validation for all API requests and responses.

### Common Schemas

#### **AgentRequestSchema**
```json
{
  "agent": "string",
  "action": "string",
  "params": "object"
}
```

#### **PipelineSchema**
```json
{
  "pipeline": ["string"],
  "input": "object"
}
```

#### **TaskResponseSchema**
```json
{
  "task_id": "string",
  "status": "string",
  "result": "object"
}
```

---

## Error Handling

All API errors follow a unified structure:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object"
  }
}
```

Common error codes:

- `AGENT_NOT_FOUND`
- `INVALID_SCHEMA`
- `PIPELINE_ERROR`
- `TASK_NOT_FOUND`
- `INTERNAL_ERROR`

---

## Future Extensions

Planned API features:

- Authentication & API keys  
- Agent sandboxing controls  
- Streaming predictor outputs  
- Multi‑pipeline orchestration  
- Remote module execution  

---

AAPP‑MART’s API layer is designed to be modular, extensible, and suitable for both local and distributed environments.  
As the framework evolves, this reference will expand with full endpoint specifications and examples.
