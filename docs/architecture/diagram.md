# System Architecture Diagram

The following diagram illustrates the high-level architecture of the project:

flowchart TD
    Client[Client / Browser] --> API[FastAPI Application]  
    API --> Validation[Pydantic Validation]  
    API --> Services[Business Logic / Services]  
    Services --> ML[Machine Learning (scikit-learn, numpy, pandas)]  
    Services --> DB[(Database)]  
    Services --> External[External APIs (httpx, requests)]  
    ML --> Visualization[Matplotlib / Seaborn / Rich CLI]  
