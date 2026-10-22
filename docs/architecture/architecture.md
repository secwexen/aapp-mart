# Architecture

This document outlines the system architecture, core components, and internal data flow.

## Project Structure

```text
aapp-mart
│   .dockerignore
│   .editorconfig
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
│           docker-image.yml
│           docker-publish.yml
│           greetings.yml
│           label.yml
│           makefile.yml
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
    │       
    ├───agents
    │       test_agents.py
    │       
    ├───api
    │       test_api.py
    │       
    ├───attack_graph
    │       test_attack_graph.py
    │       
    ├───audit
    │       test_audit.py
    │       
    ├───cli
    │       test_cli.py
    │       
    ├───cve
    │       test_cve.py
    │       
    ├───demo
    │       test_aapp_mart.py
    │       
    ├───engine
    │       test_engine.py
    │       
    ├───events
    │       test_events.py
    │       
    ├───mart
    │       test_mart.py
    │       
    ├───mitre
    │       test_mitre.py
    │       
    ├───model
    │       test_model.py
    │       
    ├───observability
    │       test_observability.py
    │       
    ├───plugins
    │       test_plugins.py
    │       
    ├───policy
    │       test_policy.py
    │       
    ├───reports
    │       test_reports.py
    │       
    ├───risk
    │       test_risk.py
    │       
    ├───runtime
    │       test_runtime.py
    │       
    ├───shared
    │       test_shared.py
    │       
    ├───simulation
    │       test_simulation.py
    │       
    ├───storage
    │       test_storage.py
    │       
    ├───threat_intel
    │       test_threat_intel.py
    │       
    └───workflows
            test_workflows.py
```
