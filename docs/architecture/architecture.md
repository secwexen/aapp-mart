# AAPP-MART Architecture

This document describes the architecture of AAPP-MART Community Edition, including its core components, supporting modules, system boundaries, and internal execution flows.

## Project Structure

```text
.
│   .dockerignore
│   .editorconfig
│   .env.example
│   .gitattributes
│   .gitignore
│   .pre-commit-config.yaml
│   ACKNOWLEDGEMENTS.md
│   CHANGELOG.md
│   CODE_OF_CONDUCT.md
│   CONTRIBUTING.md
│   DISCLAIMER.md
│   Dockerfile
│   GOVERNANCE.md
│   LICENSE
│   LICENSE‑3RD‑PARTY.md
│   MAINTAINERS
│   Makefile
│   MANIFEST.in
│   NOTICE
│   pyproject.toml
│   README.md
│   ROADMAP.md
│   SBOM.md
│   SECURITY.md
│   SUPPORT.md
│   
├───.devcontainer
│       devcontainer.json
│       Dockerfile
│       
├───.github
│   │   CODEOWNERS
│   │   dependabot.yml
│   │   FUNDING.yml
│   │   PULL_REQUEST_TEMPLATE.md
│   │   
│   ├───ISSUE_TEMPLATE
│   │       architecture_review.yml
│   │       bug_report.md
│   │       config.yml
│   │       feature_request.md
│   │       security_issue.yml
│   │       
│   └───workflows
│           ci.yml
│           codeql.yml
│           dependency-review.yml
│           docker-publish.yml
│           greetings.yml
│           label.yml
│           pylint.yml
│           python-package.yml
│           release.yml
│           secret-scan.yml
│           security.yml
│           stale.yml
│           summary.yml
│           
├───.vscode
│       extensions.json
│       settings.json
│       
├───assets
│   └───images
│           aapp-mart-logo.png
│           
├───data
│   └───samples
│           example_input.json
│           example_output.json
│           
├───demo
│       aapp_mart.py
│       
├───deployment
│   │   README.md
│   │   
│   ├───helm
│   │   └───aapp-mart
│   │           Chart.yaml
│   │           README.md
│   │           
│   └───observability
│           README.md
│           
├───docs
│   │   FAQ.md
│   │   GLOSSARY.md
│   │   README.md
│   │   
│   ├───ai
│   │       ai-powered-autonomous-attack-path-prediction.md
│   │       models.md
│   │       predictors.md
│   │       risk-model.md
│   │       
│   ├───architecture
│   │       architecture.md
│   │       components.md
│   │       design.md
│   │       modules.md
│   │       system-overview.md
│   │       threat-model.md
│   │       
│   ├───concepts
│   │       agents.md
│   │       concepts.md
│   │       
│   ├───configuration
│   │       configuration.md
│   │       
│   ├───contributing
│   │       commit-convention.md
│   │       
│   ├───executive
│   │       executive-summary.md
│   │       positioning.md
│   │       vision.md
│   │       
│   ├───getting-started
│   │       getting-started.md
│   │       installation.md
│   │       quickstart.md
│   │       
│   ├───guides
│   │       cli.md
│   │       deployment.md
│   │       development.md
│   │       troubleshooting.md
│   │       usage.md
│   │       
│   ├───legal
│   │       ethics.md
│   │       licensing.md
│   │       privacy-policy.md
│   │       terms-of-service.md
│   │       
│   ├───product
│   │       differentiators.md
│   │       examples.md
│   │       features.md
│   │       overview.md
│   │       what-is-aapp-mart.md
│   │       
│   ├───reference
│   │       api-reference.md
│   │       references.md
│   │       
│   ├───research
│   │       benchmark.md
│   │       research.md
│   │       
│   └───testing
│           testing.md
│           
├───examples
│   │   basic_simulation.py
│   │   custom_agent_example.py
│   │   integration_example.py
│   │   
│   └───reports
│           risk_summary.json
│           
├───models
│       .gitkeep
│       README.md
│       
├───observability
│   └───metrics
│           metrics.md
│           
├───scripts
│   ├───ci
│   │       lint.sh
│   │       test.sh
│   │       
│   └───dev
│           build_docs.sh
│           format_code.sh
│           run_local.py
│           
├───src
│   └───aapp_mart
│       │   py.typed
│       │   __init__.py
│       │   __main__.py
│       │   
│       ├───aapp
│       │       analyzer.py
│       │       feature_pipeline.py
│       │       models.py
│       │       prediction.py
│       │       predictor.py
│       │       scoring.py
│       │       __init__.py
│       │       
│       ├───agents
│       │       base.py
│       │       discovery.py
│       │       lateral_movement.py
│       │       privilege_escalation.py
│       │       recon.py
│       │       validation.py
│       │       __init__.py
│       │       
│       ├───api
│       │   │   app.py
│       │   │   schemas.py
│       │   │   __init__.py
│       │   │   
│       │   └───routes
│       │           attack_graph.py
│       │           prediction.py
│       │           reports.py
│       │           risk.py
│       │           simulation.py
│       │           __init__.py
│       │           
│       ├───attack_graph
│       │       builder.py
│       │       edge.py
│       │       graph.py
│       │       node.py
│       │       path_finder.py
│       │       __init__.py
│       │       
│       ├───audit
│       │       events.py
│       │       logger.py
│       │       models.py
│       │       __init__.py
│       │       
│       ├───cli
│       │   │   main.py
│       │   │   __init__.py
│       │   │   
│       │   └───commands
│       │           graph.py
│       │           predict.py
│       │           report.py
│       │           risk.py
│       │           simulate.py
│       │           __init__.py
│       │           
│       ├───cve
│       │       analyzer.py
│       │       cache.py
│       │       fetcher.py
│       │       models.py
│       │       __init__.py
│       │       
│       ├───engine
│       │       contracts.py
│       │       exceptions.py
│       │       orchestration.py
│       │       pipeline.py
│       │       state_machine.py
│       │       utils.py
│       │       __init__.py
│       │       
│       ├───events
│       │       event.py
│       │       event_types.py
│       │       publisher.py
│       │       subscriber.py
│       │       __init__.py
│       │       
│       ├───installer
│       │   │   bootstrap.py
│       │   │   environment.py
│       │   │   system_check.py
│       │   │   validator.py
│       │   │   wizard.py
│       │   │   __init__.py
│       │   │   
│       │   ├───core
│       │   │       context.py
│       │   │       executor.py
│       │   │       rollback.py
│       │   │       steps.py
│       │   │       __init__.py
│       │   │       
│       │   ├───templates
│       │   │       .env.example
│       │   │       
│       │   └───ui
│       │           console.py
│       │           __init__.py
│       │           
│       ├───mart
│       │       behavior.py
│       │       coordinator.py
│       │       state.py
│       │       strategy.py
│       │       __init__.py
│       │       
│       ├───mitre
│       │       attack_matrix.py
│       │       mapper.py
│       │       models.py
│       │       tactics.py
│       │       techniques.py
│       │       __init__.py
│       │       
│       ├───model
│       │       base.py
│       │       loader.py
│       │       manager.py
│       │       metadata.py
│       │       registry.py
│       │       __init__.py
│       │       
│       ├───observability
│       │       health.py
│       │       logging.py
│       │       metrics.py
│       │       __init__.py
│       │       
│       ├───plugins
│       │       exceptions.py
│       │       interfaces.py
│       │       loader.py
│       │       metadata.py
│       │       __init__.py
│       │       
│       ├───policy
│       │       evaluator.py
│       │       loader.py
│       │       models.py
│       │       rules.py
│       │       __init__.py
│       │       
│       ├───reports
│       │       csv_report.py
│       │       generator.py
│       │       json_report.py
│       │       models.py
│       │       __init__.py
│       │       
│       ├───risk
│       │       calculator.py
│       │       factors.py
│       │       models.py
│       │       scorer.py
│       │       __init__.py
│       │       
│       ├───runtime
│       │       context.py
│       │       execution.py
│       │       execution_result.py
│       │       __init__.py
│       │       
│       ├───shared
│       │       constants.py
│       │       utils.py
│       │       validators.py
│       │       __init__.py
│       │       
│       ├───simulation
│       │       registry.py
│       │       result.py
│       │       scenario.py
│       │       simulator.py
│       │       state.py
│       │       step.py
│       │       __init__.py
│       │       
│       ├───storage
│       │       base.py
│       │       filesystem.py
│       │       sqlite.py
│       │       __init__.py
│       │       
│       ├───threat_intel
│       │       client.py
│       │       correlation.py
│       │       feeds.py
│       │       indicators.py
│       │       models.py
│       │       __init__.py
│       │       
│       └───workflows
│               base.py
│               prediction.py
│               risk.py
│               simulation.py
│               __init__.py
│               
└───tests
    │   conftest.py
    │   
    ├───aapp
    │       test_aapp.py
    │       test_feature_pipeline.py
    │       test_prediction.py
    │       test_scoring.py
    │       
    ├───agents
    │       test_agents.py
    │       test_agent_discovery.py
    │       test_lateral_movement.py
    │       test_privilege_escalation.py
    │       test_recon.py
    │       test_validation.py
    │       
    ├───api
    │       test_api.py
    │       test_attack_graph_routes.py
    │       test_prediction_routes.py
    │       test_reports_routes.py
    │       test_risk_routes.py
    │       test_schemas.py
    │       test_simulation_routes.py
    │       
    ├───attack_graph
    │       test_attack_graph.py
    │       test_builder.py
    │       test_path_finder.py
    │       
    ├───audit
    │       test_audit.py
    │       
    ├───cli
    │       test_cli.py
    │       
    ├───compliance
    │       test_audit_compliance.py
    │       
    ├───cve
    │       test_cache.py
    │       test_cve.py
    │       test_fetcher.py
    │       
    ├───engine
    │       test_engine.py
    │       test_pipeline.py
    │       test_state_machine.py
    │       
    ├───events
    │       test_events.py
    │       
    ├───fixtures
    │       attack_graphs.py
    │       mock_services.py
    │       vulnerabilities.py
    │       
    ├───installer
    │       test_bootstrap.py
    │       test_environment.py
    │       test_rollback.py
    │       test_system_check.py
    │       test_validator.py
    │       test_wizard.py
    │       
    ├───integration
    │       test_agent_integration.py
    │       test_api_integration.py
    │       test_attack_graph_integration.py
    │       test_end_to_end.py
    │       test_plugin_integration.py
    │       test_prediction_pipeline.py
    │       test_risk_pipeline.py
    │       test_simulation_pipeline.py
    │       test_storage_integration.py
    │       
    ├───mart
    │       test_mart.py
    │       
    ├───mitre
    │       test_attack_matrix.py
    │       test_mapper.py
    │       test_mitre.py
    │       
    ├───model
    │       test_loader.py
    │       test_metadata.py
    │       test_model.py
    │       test_registry.py
    │       
    ├───observability
    │       test_observability.py
    │       
    ├───plugins
    │       test_interfaces.py
    │       test_loader.py
    │       test_plugins.py
    │       
    ├───policy
    │       test_evaluator.py
    │       test_loader.py
    │       test_policy.py
    │       test_rules.py
    │       
    ├───regression
    │       test_prediction_regression.py
    │       test_risk_regression.py
    │       
    ├───reports
    │       test_reports.py
    │       
    ├───resilience
    │       test_database_failure.py
    │       test_external_service_failure.py
    │       
    ├───risk
    │       test_risk.py
    │       
    ├───runtime
    │       test_execution.py
    │       test_runtime.py
    │       
    ├───security
    │       test_injection_protection.py
    │       test_input_validation.py
    │       test_path_traversal.py
    │       test_plugin_security.py
    │       test_sensitive_data_exposure.py
    │       test_ssrf_protection.py
    │       
    ├───shared
    │       test_shared.py
    │       
    ├───simulation
    │       test_simulation.py
    │       test_simulator.py
    │       
    ├───storage
    │       test_filesystem.py
    │       test_sqlite.py
    │       test_storage.py
    │       
    ├───threat_intel
    │       test_client.py
    │       test_correlation.py
    │       test_feeds.py
    │       test_threat_intel.py
    │       
    └───workflows
            test_prediction_workflow.py
            test_risk_workflow.py
            test_simulation_workflow.py
            test_workflows.py
```

## Architecture Diagram

This diagram illustrates the AAPP-MART Community Edition architecture, highlighting ENGINE orchestration, AAPP prediction, MART simulation, and supporting modules.

```mermaid
flowchart TB

    %% =========================================================
    %% CLIENT / ACCESS LAYER
    %% =========================================================

    subgraph ACCESS["Client / Access Layer"]
        direction LR

        USER["Users / Administrators"]
        CLI["Command Line Interface"]
        API["Basic API"]

        USER --> CLI
        USER --> API
    end

    %% =========================================================
    %% COMMUNITY EDITION
    %% =========================================================

    subgraph COMMUNITY["AAPP-MART Community Edition"]
        direction TB

        %% =====================================================
        %% ENGINE - CORE ORCHESTRATION
        %% =====================================================

        subgraph ENGINE["ENGINE - Core Orchestration"]
            direction TB

            ENTRY["Execution Entry Point"]
            PIPELINE["Execution Pipeline"]
            CONTRACTS["Shared Execution Contracts"]
            RUNTIME["Runtime Manager"]
            STATE["Execution State Machine"]
            EXCEPTIONS["Execution Error Handling"]

            ENTRY --> PIPELINE
            PIPELINE --> CONTRACTS
            PIPELINE --> RUNTIME
            RUNTIME --> STATE
            PIPELINE -.-> EXCEPTIONS
        end

        %% =====================================================
        %% AAPP - AI-POWERED AUTONOMOUS ATTACK PATH PREDICTION
        %% =====================================================

        subgraph AAPP["AAPP - AI-Powered Autonomous Attack Path Prediction"]
            direction TB

            subgraph ATTACK_GRAPH["Attack Graph Analysis"]
                direction LR

                GRAPH_BUILDER["Attack Graph Builder"]
                GRAPH_MODELS["Graph / Node / Edge Models"]
                PATH_FINDER["Attack Path Finder"]

                GRAPH_BUILDER --> GRAPH_MODELS
                GRAPH_MODELS --> PATH_FINDER
            end

            subgraph AAPP_ANALYSIS["Prediction Analysis"]
                direction LR

                ANALYZER["Attack Graph Analyzer"]
                FEATURES["Feature Pipeline"]
                PREDICTOR["Pluggable Prediction Backend"]
                PREDICTION["Prediction Orchestrator"]

                ANALYZER --> FEATURES
                FEATURES --> PREDICTOR
                PREDICTOR --> PREDICTION
            end

            SCORING["AAPP Risk Scoring"]

            ATTACK_GRAPH --> ANALYZER
            PREDICTION --> SCORING
        end

        %% =====================================================
        %% MART - MULTI-AGENT RED TEAM SIMULATION
        %% =====================================================

        subgraph MART["MART - Multi-Agent Red Team Simulation"]
            direction TB

            subgraph AGENT_LAYER["Agent Management"]
                direction LR

                AGENT_BASE["Base Agent"]
                RECON["Recon Agent"]
                DISCOVERY["Discovery Agent"]
                LATERAL["Lateral Movement Agent"]
                PRIVILEGE["Privilege Escalation Agent"]
                VALIDATION_AGENT["Validation Agent"]

                AGENT_BASE --> RECON
                AGENT_BASE --> DISCOVERY
                AGENT_BASE --> LATERAL
                AGENT_BASE --> PRIVILEGE
                AGENT_BASE --> VALIDATION_AGENT
            end

            subgraph MART_COORDINATION["Agent Coordination"]
                direction LR

                COORDINATOR["Agent Coordinator"]
                STRATEGY["Agent Strategy"]
                BEHAVIOR["Agent Behavior"]
                MART_STATE["Agent State"]

                COORDINATOR --> STRATEGY
                STRATEGY --> BEHAVIOR
                BEHAVIOR --> MART_STATE
            end

            subgraph SIMULATION["Simulation Environment"]
                direction LR

                SCENARIO["Scenario Management"]
                SIMULATOR["Simulation Engine"]
                SIM_STATE["Simulation State"]
                SIM_STEP["Simulation Step"]
                SIM_RESULT["Simulation Result"]

                SCENARIO --> SIMULATOR
                SIMULATOR --> SIM_STATE
                SIMULATOR --> SIM_STEP
                SIMULATOR --> SIM_RESULT
            end

            AGENT_LAYER --> MART_COORDINATION
            MART_COORDINATION --> SIMULATION

            %% Agent decision cycle and environment feedback
            SIMULATION -.-> MART_COORDINATION
        end

        %% =====================================================
        %% MITRE ATT&CK MAPPING
        %% =====================================================

        subgraph MITRE["MITRE ATT&CK Mapping"]
            direction LR

            ATTACK_MATRIX["ATT&CK Matrix"]
            TACTICS["Tactics"]
            TECHNIQUES["Techniques"]
            MITRE_MAPPER["ATT&CK Mapper"]

            ATTACK_MATRIX --> TACTICS
            ATTACK_MATRIX --> TECHNIQUES
            TACTICS --> MITRE_MAPPER
            TECHNIQUES --> MITRE_MAPPER
        end

        %% =====================================================
        %% CVE ANALYSIS
        %% =====================================================

        subgraph CVE["CVE Analysis"]
            direction LR

            CVE_FETCHER["CVE Fetcher"]
            CVE_ANALYZER["CVE Analyzer"]
            CVE_MODELS["CVE Models"]
            CVE_CACHE["CVE Cache"]

            CVE_FETCHER --> CVE_ANALYZER
            CVE_ANALYZER --> CVE_MODELS
            CVE_FETCHER --> CVE_CACHE
        end

        %% =====================================================
        %% THREAT INTELLIGENCE
        %% =====================================================

        subgraph THREAT_INTEL["Basic Threat Intelligence - Public Sources"]
            direction LR

            TI_CLIENT["Threat Intelligence Client"]
            TI_FEEDS["Public Threat Feeds"]
            TI_INDICATORS["Threat Indicators"]
            TI_CORRELATION["Threat Correlation"]

            TI_CLIENT --> TI_FEEDS
            TI_FEEDS --> TI_INDICATORS
            TI_INDICATORS --> TI_CORRELATION
        end

        %% =====================================================
        %% RISK ASSESSMENT
        %% =====================================================

        subgraph RISK["Risk Assessment"]
            direction LR

            RISK_MODELS["Risk Models"]
            RISK_FACTORS["Risk Factors"]
            RISK_CALCULATOR["Risk Calculator"]
            RISK_SCORER["Risk Scorer"]

            RISK_MODELS --> RISK_CALCULATOR
            RISK_FACTORS --> RISK_CALCULATOR
            RISK_CALCULATOR --> RISK_SCORER
        end

        %% =====================================================
        %% POLICY EVALUATION
        %% =====================================================

        subgraph POLICY["Core Policy Evaluation"]
            direction LR

            POLICY_MODELS["Policy Models"]
            POLICY_LOADER["Policy Loader"]
            POLICY_RULES["Policy Rules"]
            POLICY_EVALUATOR["Policy Evaluator"]

            POLICY_LOADER --> POLICY_MODELS
            POLICY_MODELS --> POLICY_EVALUATOR
            POLICY_RULES --> POLICY_EVALUATOR
        end

        %% =====================================================
        %% WORKFLOW ORCHESTRATION
        %% =====================================================

        subgraph WORKFLOWS["Workflow Orchestration"]
            direction LR

            WORKFLOW_BASE["Workflow Base"]
            PREDICTION_WORKFLOW["Prediction Workflow"]
            RISK_WORKFLOW["Risk Workflow"]
            SIMULATION_WORKFLOW["Simulation Workflow"]

            WORKFLOW_BASE --> PREDICTION_WORKFLOW
            WORKFLOW_BASE --> RISK_WORKFLOW
            WORKFLOW_BASE --> SIMULATION_WORKFLOW
        end

        %% =====================================================
        %% MODEL MANAGEMENT
        %% =====================================================

        subgraph MODEL_MANAGEMENT["Core Model Management"]
            direction LR

            MODEL_BASE["Model Base"]
            MODEL_LOADER["Model Loader"]
            MODEL_MANAGER["Model Manager"]
            MODEL_REGISTRY["Model Registry"]
            MODEL_METADATA["Model Metadata"]

            MODEL_BASE --> MODEL_MANAGER
            MODEL_MANAGER --> MODEL_LOADER
            MODEL_MANAGER --> MODEL_REGISTRY
            MODEL_REGISTRY --> MODEL_METADATA
        end

        %% =====================================================
        %% PLUGIN ARCHITECTURE
        %% =====================================================

        subgraph PLUGINS["Core Plugin Architecture"]
            direction LR

            PLUGIN_INTERFACES["Plugin Interfaces"]
            PLUGIN_METADATA["Plugin Metadata"]
            PLUGIN_LOADER["Plugin Loader"]
            PLUGIN_EXCEPTIONS["Plugin Exceptions"]

            PLUGIN_INTERFACES --> PLUGIN_LOADER
            PLUGIN_LOADER --> PLUGIN_METADATA
            PLUGIN_LOADER -.-> PLUGIN_EXCEPTIONS
        end

        %% =====================================================
        %% REPORTING
        %% =====================================================

        subgraph REPORTING["JSON / CSV Reporting"]
            direction LR

            REPORT_MODELS["Report Models"]
            REPORT_GENERATOR["Report Generator"]
            JSON_REPORT["JSON Report Export"]
            CSV_REPORT["CSV Report Export"]

            REPORT_MODELS --> REPORT_GENERATOR
            REPORT_GENERATOR --> JSON_REPORT
            REPORT_GENERATOR --> CSV_REPORT
        end

        %% =====================================================
        %% STORAGE
        %% =====================================================

        subgraph STORAGE["Storage Infrastructure"]
            direction LR

            STORAGE_BASE["Storage Interface"]
            FILESYSTEM["Filesystem Storage"]
            SQLITE["SQLite Storage"]

            STORAGE_BASE --> FILESYSTEM
            STORAGE_BASE --> SQLITE
        end

        %% =====================================================
        %% SHARED INFRASTRUCTURE
        %% =====================================================

        subgraph SHARED["Shared Infrastructure"]
            direction TB

            VALIDATORS["Shared Input Validators"]
            CONSTANTS["Shared Constants"]
            UTILS["Shared Utilities"]

            subgraph EVENT_SYSTEM["Event System"]
                direction LR

                EVENT_TYPES["Event Types"]
                EVENT_PUBLISHER["Event Publisher"]
                EVENT_SUBSCRIBER["Event Subscribers"]

                EVENT_TYPES --> EVENT_PUBLISHER
                EVENT_PUBLISHER --> EVENT_SUBSCRIBER
            end

            subgraph OBSERVABILITY["Basic Observability"]
                direction LR

                LOGGING["Logging"]
                METRICS["Metrics"]
                HEALTH["Health Monitoring"]
            end

            subgraph AUDIT["Basic Audit Logging"]
                direction LR

                AUDIT_EVENTS["Audit Events"]
                AUDIT_MODELS["Audit Models"]
                AUDIT_LOGGER["Audit Logger"]

                AUDIT_EVENTS --> AUDIT_MODELS
                AUDIT_MODELS --> AUDIT_LOGGER
            end
        end

        %% =====================================================
        %% CORE EXECUTION INTEGRATION
        %% =====================================================

        PIPELINE --> PREDICTION
        PIPELINE --> SIMULATOR

        %% =====================================================
        %% SECURITY INTELLIGENCE INTEGRATION
        %% =====================================================

        MITRE_MAPPER -.-> MART
        MITRE_MAPPER -.-> ATTACK_GRAPH

        CVE_ANALYZER -.-> ATTACK_GRAPH
        TI_CORRELATION -.-> ATTACK_GRAPH

        %% =====================================================
        %% RISK INTEGRATION
        %% =====================================================

        SCORING -.-> RISK_SCORER
        CVE_ANALYZER -.-> RISK_SCORER
        TI_CORRELATION -.-> RISK_SCORER

        %% =====================================================
        %% POLICY INTEGRATION
        %% =====================================================

        POLICY_EVALUATOR -.-> PIPELINE

        %% =====================================================
        %% WORKFLOW INTEGRATION
        %% =====================================================

        PIPELINE -.-> WORKFLOW_BASE

        PREDICTION_WORKFLOW -.-> PREDICTION
        RISK_WORKFLOW -.-> RISK_SCORER
        SIMULATION_WORKFLOW -.-> SIMULATOR

        %% =====================================================
        %% MODEL MANAGEMENT INTEGRATION
        %% =====================================================

        MODEL_MANAGER -.-> PREDICTOR

        %% =====================================================
        %% PLUGIN EXTENSION POINTS
        %% =====================================================

        PLUGIN_LOADER -.-> ENGINE
        PLUGIN_LOADER -.-> AAPP
        PLUGIN_LOADER -.-> MART

        %% =====================================================
        %% VALIDATION AND SHARED SERVICES
        %% =====================================================

        VALIDATORS -.-> ENGINE
        VALIDATORS -.-> AAPP
        VALIDATORS -.-> MART

        CONSTANTS -.-> ENGINE
        UTILS -.-> ENGINE

        %% =====================================================
        %% EVENT AND OBSERVABILITY INTEGRATION
        %% =====================================================

        PIPELINE --> EVENT_PUBLISHER
        RUNTIME --> EVENT_PUBLISHER

        EVENT_SUBSCRIBER -.-> OBSERVABILITY
        EVENT_SUBSCRIBER -.-> AUDIT

        %% =====================================================
        %% STORAGE INTEGRATION
        %% =====================================================

        STORAGE_BASE -.-> REPORTING
        STORAGE_BASE -.-> MODEL_MANAGEMENT

        %% =====================================================
        %% REPORTING INTEGRATION
        %% =====================================================

        PREDICTION -.-> REPORT_GENERATOR
        SIM_RESULT -.-> REPORT_GENERATOR
        RISK_SCORER -.-> REPORT_GENERATOR

    end

    %% =========================================================
    %% ACCESS INTEGRATION
    %% =========================================================

    CLI --> ENTRY
    API --> ENTRY

    %% =========================================================
    %% COMPONENT STYLING
    %% =========================================================

    classDef access fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef engine fill:#d1fae5,stroke:#059669,color:#064e3b
    classDef aapp fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef mart fill:#ffedd5,stroke:#ea580c,color:#7c2d12
    classDef security fill:#fee2e2,stroke:#dc2626,color:#7f1d1d
    classDef governance fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef shared fill:#f3f4f6,stroke:#6b7280,color:#1f2937
    classDef extension fill:#fce7f3,stroke:#db2777,color:#831843

    class USER,CLI,API access

    class ENTRY,PIPELINE,CONTRACTS,RUNTIME,STATE,EXCEPTIONS engine

    class GRAPH_BUILDER,GRAPH_MODELS,PATH_FINDER,ANALYZER,FEATURES,PREDICTOR,PREDICTION,SCORING aapp

    class AGENT_BASE,RECON,DISCOVERY,LATERAL,PRIVILEGE,VALIDATION_AGENT,COORDINATOR,STRATEGY,BEHAVIOR,MART_STATE,SIMULATOR,SCENARIO,SIM_STATE,SIM_STEP,SIM_RESULT mart

    class ATTACK_MATRIX,TACTICS,TECHNIQUES,MITRE_MAPPER,CVE_FETCHER,CVE_ANALYZER,CVE_MODELS,CVE_CACHE,TI_CLIENT,TI_FEEDS,TI_INDICATORS,TI_CORRELATION security

    class RISK_MODELS,RISK_FACTORS,RISK_CALCULATOR,RISK_SCORER,POLICY_MODELS,POLICY_LOADER,POLICY_RULES,POLICY_EVALUATOR governance

    class WORKFLOW_BASE,PREDICTION_WORKFLOW,RISK_WORKFLOW,SIMULATION_WORKFLOW governance

    class MODEL_BASE,MODEL_LOADER,MODEL_MANAGER,MODEL_REGISTRY,MODEL_METADATA governance

    class PLUGIN_INTERFACES,PLUGIN_METADATA,PLUGIN_LOADER,PLUGIN_EXCEPTIONS extension

    class REPORT_MODELS,REPORT_GENERATOR,JSON_REPORT,CSV_REPORT governance

    class STORAGE_BASE,FILESYSTEM,SQLITE governance

    class VALIDATORS,CONSTANTS,UTILS,EVENT_TYPES,EVENT_PUBLISHER,EVENT_SUBSCRIBER,LOGGING,METRICS,HEALTH,AUDIT_EVENTS,AUDIT_MODELS,AUDIT_LOGGER shared

    %% =====================================================
    %% SUBGRAPH STYLING
    %% =====================================================

    style ACCESS fill:#eff6ff,stroke:#2563eb,stroke-width:2px
    style COMMUNITY fill:#ffffff,stroke:#334155,stroke-width:3px
    style ENGINE fill:#ecfdf5,stroke:#059669,stroke-width:2px
    style AAPP fill:#f5f3ff,stroke:#7c3aed,stroke-width:2px
    style MART fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style ATTACK_GRAPH fill:#faf5ff,stroke:#8b5cf6,stroke-width:1.5px
    style AAPP_ANALYSIS fill:#faf5ff,stroke:#8b5cf6,stroke-width:1.5px
    style AGENT_LAYER fill:#fff7ed,stroke:#f97316,stroke-width:1.5px
    style MART_COORDINATION fill:#fff7ed,stroke:#f97316,stroke-width:1.5px
    style SIMULATION fill:#fff7ed,stroke:#f97316,stroke-width:1.5px
    style MITRE fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style CVE fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style THREAT_INTEL fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style RISK fill:#fffbeb,stroke:#d97706,stroke-width:2px
    style POLICY fill:#fffbeb,stroke:#d97706,stroke-width:2px
    style WORKFLOWS fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style MODEL_MANAGEMENT fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px
    style PLUGINS fill:#fdf2f8,stroke:#db2777,stroke-width:2px
    style REPORTING fill:#f1f5f9,stroke:#64748b,stroke-width:2px
    style STORAGE fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style SHARED fill:#f9fafb,stroke:#6b7280,stroke-width:2px
    style EVENT_SYSTEM fill:#ffffff,stroke:#9ca3af,stroke-width:1px
    style OBSERVABILITY fill:#ffffff,stroke:#9ca3af,stroke-width:1px
    style AUDIT fill:#ffffff,stroke:#9ca3af,stroke-width:1px
```
