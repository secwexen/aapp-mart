# System Architecture Diagram

The following diagram illustrates the high-level architecture of the project:

```mermaid
flowchart TD
    Client[Client / Browser] --> API[FastAPI Application]

    API --> Validation[Pydantic Validation Layer]
    API --> Services[Business Logic Layer / Services]

    Services --> ML[Machine Learning Layer<br/>(scikit-learn, NumPy, pandas)]
    Services --> DB[(Database)]
    Services --> External[External APIs<br/>(httpx, requests)]

    ML --> Visualization[Visualization Layer<br/>(Matplotlib / Seaborn / Rich CLI)]
```
