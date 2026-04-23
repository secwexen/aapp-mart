# AAPP-MART Demo

This folder contains a minimal runnable example of the AAPP-MART system.

## Purpose

The demo shows how to:
- Initialize the attack path simulation engine
- Run a basic simulation
- Export a sample report

This is intended for quick testing and validation.

## How to run

From the project root:

```bash
python demo/attack_simulation_demo.py
```

## Expected Output

When running successfully, you should see:

- Target initialization
- Simulation steps (recon, attack path generation, risk scoring)
- Report export confirmation

## Notes

- If the `aapp_mart` package is not installed, the demo will run in **DEMO MODE**
- No external dependencies are required for basic demonstration
- This script is safe and uses only simulated logic if core modules are missing

## Related

- Main project: [./README.md](https://github.com/secwexen/aapp-mart/blob/main/README.md)
- Demo notebook: [aapp-mart/demo/attack_path_demo.ipynb](https://github.com/secwexen/aapp-mart/blob/main/demo/attack_path_demo.ipynb)
