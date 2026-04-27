# Restaurant POS Sales Reporting
A command-line Python Point-of-Sale (POS) and Sales Reporting Tool for capturing Customer Orders, calculating Order Totals, generating receipts, and producing an end-of-day (EOD) Sales Report.

## Project Status
Initial rebuild complete (2026-04-27).

This project began as an early Python script and has been refactored into a cleaner small-business reporting tool. The current version includes structured menu items, transaction-level order tracking, receipt generation, item-level sales summaries, category-level revenue reporting, and basic input validation.

## Business Problem
Small restaurants need a simple way to capture orders, calculate totals, and summarize daily sales activity. This project demonstrates how a lightweight Python application can support point-of-sale workflows and basic sales reporting.

## Current Features
- Captures customer burger orders through a command-line workflow.
- Stores menu items using a Python `dataclass`.
- Tracks each customer order as a transaction.
- Calculates order totals.
- Generates formatted customer receipts.
- Produces an end-of-day sales report.
- Summarizes quantity and revenue by menu item.
- Summarizes revenue by menu category.
- Calculates total orders, total revenue, and average order value.
- Includes basic input validation for menu choices.

## Tools
- Python
- Standard library only

## Example Use Case
A small restaurant operator wants a simple way to capture orders during service and review end-of-day performance. By entering each customer order, the tool produces receipts and summarizes sales by item, category, total revenue, and average order value.

## Planned Improvements
- Add CSV export for transaction history.
- Add menu customization through an external file.
- Add unit tests.
- Add sample output files.
- Add sales visualizations.
- Add support for item quantities greater than one.
- Add optional tax and tip calculations.

## Project Structure
```text
restaurant-pos-sales-reporting/
├── RestaurantPOSSalesReporting.py
└── README.md
```

## Notes
This project is part of my Python Automation Lab and represents a refactored version of an early Python point-of-sale exercise.
