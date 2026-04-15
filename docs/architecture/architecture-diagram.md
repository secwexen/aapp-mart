# System Architecture Diagram

The following diagram illustrates the high-level architecture of the project:

```mermaid
flowchart TD
    Client[Client / Browser] --> API[FastAPI Application]

    API --> Validation[Pydantic Validation Layer]
    API --> Services[Business Logic Layer / Services]

    Services --> ML[Machine Learning Layer]
    Services --> DB[Database]
    Services --> External[External APIs]

    ML --> Visualization[Visualization Layer]
```
