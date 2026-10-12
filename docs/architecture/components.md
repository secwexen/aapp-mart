# Core Components

This document describes the three major subsystems of AAPP-MART: AI-Powered Autonomous Attack Path Prediction (AAPP), Multi-Agent Red Team Simulation (MART), and Core Orchestration (ENGINE).

It outlines their responsibilities, relationships, and roles within the overall architecture.

## AI-Powered Autonomous Attack Path Prediction (AAPP)

Predicts the most likely attack paths by analyzing services, permissions, vulnerabilities, and configuration weaknesses.

## Multi-Agent Red Team Simulation (MART)

Executes autonomous red team simulations using specialized AI agents that emulate real attacker behavior.

Together, AAPP and MART create a fully automated offensive security engine capable of forecasting and simulating attacks end-to-end.

## Core Orchestration (ENGINE)

The CORE engine coordinates multi-agent behavior, manages simulation flow, and ensures consistent interaction between all system modules.

## Component Interaction

ENGINE coordinates the overall workflow. AAPP supports attack-path and risk analysis, while MART handles the simulation workflows supported by the implementation.

Actual capabilities depend on the implemented modules and their tests.
