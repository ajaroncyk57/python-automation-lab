# Mortgage Affordability Analyzer

A command-line Python personal finance tool for evaluating home affordability using mortgage payment calculations, debt-to-income ratios, monthly budget assumptions, rate stress tests, and maximum purchase price estimates.

## Project Status

Initial build complete (2026-04-27).

This project began as an early mortgage and budget calculator and has been expanded into a more practical affordability analysis tool. The current version evaluates mortgage payments, estimated housing costs, monthly budget fit, affordability ratios, interest-rate sensitivity, and estimated maximum purchase price under a 30% housing-cost benchmark.

## Business Problem

Home affordability depends on more than the monthly principal and interest payment. Buyers also need to consider property taxes, insurance, HOA or condo fees, PMI, other monthly expenses, debt payments, and how sensitive the budget is to changes in interest rates. This project demonstrates how Python can support practical personal finance decision-making by combining mortgage math with budget analysis.

## Current Features

- Collects mortgage assumptions through a command-line workflow.
- Collects household income and expense assumptions.
- Stores mortgage and budget inputs using Python `dataclass` objects.
- Calculates loan amount and down payment percentage.
- Calculates monthly principal and interest payment.
- Estimates monthly property tax, insurance, HOA/condo fees, and PMI.
- Calculates total monthly housing cost.
- Calculates total monthly expenses including housing.
- Calculates estimated monthly cash leftover.
- Calculates front-end and back-end debt-to-income ratios.
- Calculates total principal and interest paid over the life of the loan.
- Calculates total interest paid.
- Classifies affordability using common DTI-style thresholds.
- Runs interest-rate stress tests.
- Estimates maximum purchase price under a 30% monthly housing-cost benchmark.
- Uses only the Python standard library.

## Tools

- Python
- Standard library only

## Example Use Case

A prospective homebuyer wants to evaluate whether a home or condo fits their monthly budget. By entering purchase price, down payment, rate, term, taxes, insurance, HOA fees, PMI, income, and expenses, the tool produces a mortgage affordability report, rate stress test, and estimated maximum purchase price target.

## Planned Improvements

- Add CSV export for affordability reports and stress-test scenarios.
- Add support for property appreciation and home equity estimates.
- Add amortization schedule output.
- Add visualization support for principal, interest, and remaining balance over time.
- Add unit tests.
- Add sample output files.
- Add optional comparison of multiple home purchase scenarios.
- Add net income / take-home pay assumptions.

## Project Structure

```text
mortgage-affordability-analyzer/
├── MortgageAffordabilityAnalyzer.py
└── README.md
```

## Notes

This project is part of my Python Automation Lab and represents a refactored, expanded version of an early mortgage and monthly budget calculator.
