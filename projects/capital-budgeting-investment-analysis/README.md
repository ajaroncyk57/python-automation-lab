# Capital Budgeting Investment Analysis

A command-line Python tool for evaluating Capital Budgeting Projects using core finance metrics, including Net Present Value (NPV), Internal Rate of Return (IRR), Return on Investment (ROI), Payback Period, and Profitability Index.

## Project Status

Initial rebuild complete (2026-04-24).

This project began as an early Python script and has been refactored into a cleaner command-line finance analytics tool. The current version includes reusable functions, structured project assumptions, input validation, investment metric calculations, and a formatted investment report.

## Business Problem

Capital Budgeting decisions require comparing upfront Investment Costs against expected Future Cash Flows. This project helps evaluate whether a proposed investment is financially attractive based on user-provided assumptions such as Initial Investment, expected Annual Cash Inflows, annual Cash Outflows, Project Lifetime, and Required Rate of Return.

## Current Features

- Collects project assumptions from user input.
- Stores assumptions using a Python `dataclass`.
- Calculates Net Present Value (NPV).
- Estimates Internal Rate of Return (IRR) using the Bisection Method.
- Calculates Return on Investment (ROI).
- Calculates Payback Period.
- Calculates Profitability Index.
- Generates a formatted Investment Analysis Report.
- Provides an investment recommendation based on NPV and IRR.
- Includes basic input validation for numeric values.

## Tools

- Python
- Standard library only

## Example Use Case

A business stakeholder is evaluating whether to invest in a new project, system, product line, or operational improvement. By entering expected investment costs and projected annual cash flows, the tool produces a financial summary that can support an accept, reject, or further-review decision.

## Planned Improvements

- Add scenario analysis for best-case, base-case, and worst-case assumptions.
- Add CSV input/output.
- Add unit tests.
- Add sample output files.
- Add visualizations for projected cash flows and cumulative payback.
- Create a more detailed project walkthrough.

## Project Structure

```text
capital-budgeting-investment-analysis/
├── CapitalBudgeting.py
└── README.md
