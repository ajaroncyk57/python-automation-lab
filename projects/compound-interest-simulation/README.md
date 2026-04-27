# Compound Interest Scenario Simulator

A command-line Python finance analytics tool for projecting investment growth using deterministic compound interest and Monte Carlo simulation.

## Project Status

Initial build complete (2026-04-27).

This project began as a simple compound-interest loop and has been expanded into a more robust investment scenario simulator. The current version includes year-by-year projections, annual contributions, inflation-adjusted balances, Monte Carlo simulation, percentile outcomes, target-balance probability estimates, and optional CSV export.

## Business Problem

Investors and analysts often need to understand how an investment may grow over time under both expected and uncertain return assumptions. This project demonstrates how Python can be used to model deterministic growth, simulate risk, and summarize possible investment outcomes in a decision-friendly format.

## Current Features

- Collects investment assumptions through a command-line workflow.
- Stores inputs using Python `dataclass` objects.
- Builds a deterministic year-by-year compound interest projection.
- Supports annual contributions.
- Calculates inflation-adjusted ending balances.
- Runs Monte Carlo simulations using normally distributed annual returns.
- Calculates average, median, standard deviation, and percentile outcomes.
- Estimates the probability of reaching a user-defined target balance.
- Prints formatted projection and simulation summary reports.
- Optionally exports projection and simulation summary results to CSV.
- Uses only the Python standard library.

## Tools

- Python
- Standard library only

## Example Use Case

A user wants to evaluate how an investment might grow over a long-term time horizon while accounting for expected returns, volatility, inflation, annual contributions, and a target ending balance. The tool produces both a deterministic projection and a simulated range of potential outcomes.

## Planned Improvements

- Add support for monthly contributions and monthly compounding.
- Add scenario comparison for conservative, base-case, and aggressive return assumptions.
- Add visualization support for projection paths and simulation distributions.
- Add unit tests.
- Add sample output files.
- Add optional CSV import for assumption sets.
- Add a richer risk summary with downside probability and value-at-risk style metrics.

## Project Structure

```text
compound-interest-simulation/
├── CompoundInterestSimulator.py
└── README.md
```

## Notes

This project is part of my Python Automation Lab and represents a refactored, expanded version of an early compound interest exercise.
