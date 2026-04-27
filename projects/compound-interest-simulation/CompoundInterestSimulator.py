"""
Compound Interest Scenario Simulator

A command-line Python tool for projecting investment growth using deterministic
compound interest and Monte Carlo simulation.

This project expands a basic compound-interest loop into a more portfolio-ready
finance analytics tool with scenario analysis, simulated returns, probability
estimates, percentile outcomes, and optional CSV export.

Author: Andrew Jaroncyk
"""

from dataclasses import dataclass
from pathlib import Path
from random import normalvariate, seed
from statistics import mean, median, stdev
from typing import Dict, List, Optional
import csv


@dataclass
class InvestmentAssumptions:
    """Stores the assumptions used for the investment projection."""

    starting_balance: float
    annual_contribution: float
    years: int
    expected_annual_return: float
    annual_volatility: float
    annual_inflation_rate: float
    target_balance: float
    simulations: int


@dataclass
class YearlyProjection:
    """Stores projected investment values for one year."""

    year: int
    starting_balance: float
    contribution: float
    investment_return: float
    ending_balance: float
    inflation_adjusted_balance: float


@dataclass
class SimulationSummary:
    """Stores Monte Carlo simulation summary statistics."""

    simulations: int
    average_final_balance: float
    median_final_balance: float
    standard_deviation: float
    percentile_10: float
    percentile_25: float
    percentile_75: float
    percentile_90: float
    probability_reaching_target: float


def format_currency(value: float) -> str:
    """Formats a numeric value as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Formats a decimal value as a percentage."""
    return f"{value * 100:.2f}%"


def get_float_input(prompt: str, minimum: Optional[float] = None) -> float:
    """Safely collects a numeric input from the user."""
    while True:
        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Please enter a value greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def get_int_input(prompt: str, minimum: Optional[int] = None) -> int:
    """Safely collects an integer input from the user."""
    while True:
        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Please enter a value greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")


def get_yes_no(prompt: str) -> bool:
    """Collects a yes/no response from the user."""
    while True:
        choice = input(prompt).strip().lower()

        if choice in {"y", "yes"}:
            return True

        if choice in {"n", "no"}:
            return False

        print("Please enter Y or N.")


def collect_investment_assumptions() -> InvestmentAssumptions:
    """Collects investment projection assumptions from the user."""
    print("\nCompound Interest Scenario Simulator")
    print("-" * 50)

    starting_balance = get_float_input(
        "Enter starting investment balance: $",
        minimum=0,
    )

    annual_contribution = get_float_input(
        "Enter expected annual contribution: $",
        minimum=0,
    )

    years = get_int_input(
        "Enter investment time horizon in years: ",
        minimum=1,
    )

    expected_annual_return = get_float_input(
        "Enter expected annual return as a decimal, e.g. 0.07 for 7%: ",
        minimum=-0.99,
    )

    annual_volatility = get_float_input(
        "Enter expected annual volatility as a decimal, e.g. 0.15 for 15%: ",
        minimum=0,
    )

    annual_inflation_rate = get_float_input(
        "Enter annual inflation rate as a decimal, e.g. 0.03 for 3%: ",
        minimum=0,
    )

    target_balance = get_float_input(
        "Enter target ending balance: $",
        minimum=0,
    )

    simulations = get_int_input(
        "Enter number of Monte Carlo simulations, e.g. 1000: ",
        minimum=100,
    )

    return InvestmentAssumptions(
        starting_balance=starting_balance,
        annual_contribution=annual_contribution,
        years=years,
        expected_annual_return=expected_annual_return,
        annual_volatility=annual_volatility,
        annual_inflation_rate=annual_inflation_rate,
        target_balance=target_balance,
        simulations=simulations,
    )


def calculate_inflation_adjusted_value(
    future_value: float,
    inflation_rate: float,
    year: int,
) -> float:
    """Converts a future balance into today's dollars."""
    return future_value / ((1 + inflation_rate) ** year)


def build_deterministic_projection(
    assumptions: InvestmentAssumptions,
) -> List[YearlyProjection]:
    """Builds a year-by-year investment projection using expected return."""
    projections: List[YearlyProjection] = []
    balance = assumptions.starting_balance

    for year in range(1, assumptions.years + 1):
        starting_balance = balance
        contribution = assumptions.annual_contribution
        investment_return = (starting_balance + contribution) * assumptions.expected_annual_return
        ending_balance = starting_balance + contribution + investment_return
        inflation_adjusted_balance = calculate_inflation_adjusted_value(
            ending_balance,
            assumptions.annual_inflation_rate,
            year,
        )

        projections.append(
            YearlyProjection(
                year=year,
                starting_balance=starting_balance,
                contribution=contribution,
                investment_return=investment_return,
                ending_balance=ending_balance,
                inflation_adjusted_balance=inflation_adjusted_balance,
            )
        )

        balance = ending_balance

    return projections


def run_single_simulation(assumptions: InvestmentAssumptions) -> float:
    """Runs one simulated investment path and returns final balance."""
    balance = assumptions.starting_balance

    for _ in range(assumptions.years):
        simulated_return = normalvariate(
            assumptions.expected_annual_return,
            assumptions.annual_volatility,
        )
        simulated_return = max(simulated_return, -0.99)
        balance = (balance + assumptions.annual_contribution) * (1 + simulated_return)

    return balance


def percentile(values: List[float], percentile_rank: float) -> float:
    """Calculates a percentile using linear interpolation."""
    if not values:
        raise ValueError("Cannot calculate percentile of an empty list.")

    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * percentile_rank
    lower_index = int(index)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = index - lower_index

    return (
        sorted_values[lower_index] * (1 - weight)
        + sorted_values[upper_index] * weight
    )


def run_monte_carlo_simulation(
    assumptions: InvestmentAssumptions,
    random_seed: int = 57,
) -> List[float]:
    """Runs Monte Carlo simulations and returns final balances."""
    seed(random_seed)
    return [run_single_simulation(assumptions) for _ in range(assumptions.simulations)]


def summarize_simulation_results(
    final_balances: List[float],
    target_balance: float,
) -> SimulationSummary:
    """Summarizes Monte Carlo final balance results."""
    if len(final_balances) < 2:
        raise ValueError("At least two simulations are required for summary statistics.")

    target_hits = sum(balance >= target_balance for balance in final_balances)

    return SimulationSummary(
        simulations=len(final_balances),
        average_final_balance=mean(final_balances),
        median_final_balance=median(final_balances),
        standard_deviation=stdev(final_balances),
        percentile_10=percentile(final_balances, 0.10),
        percentile_25=percentile(final_balances, 0.25),
        percentile_75=percentile(final_balances, 0.75),
        percentile_90=percentile(final_balances, 0.90),
        probability_reaching_target=target_hits / len(final_balances),
    )


def print_deterministic_projection(projections: List[YearlyProjection]) -> None:
    """Prints the deterministic year-by-year projection."""
    print("\nDeterministic Projection")
    print("=" * 90)
    print(
        f"{'Year':<6}"
        f"{'Start Balance':>18}"
        f"{'Contribution':>18}"
        f"{'Return':>16}"
        f"{'End Balance':>18}"
        f"{'Inflation Adj.':>18}"
    )
    print("-" * 90)

    for row in projections:
        print(
            f"{row.year:<6}"
            f"{format_currency(row.starting_balance):>18}"
            f"{format_currency(row.contribution):>18}"
            f"{format_currency(row.investment_return):>16}"
            f"{format_currency(row.ending_balance):>18}"
            f"{format_currency(row.inflation_adjusted_balance):>18}"
        )

    print("=" * 90)


def print_simulation_summary(summary: SimulationSummary, target_balance: float) -> None:
    """Prints Monte Carlo simulation summary statistics."""
    print("\nMonte Carlo Simulation Summary")
    print("=" * 70)
    print(f"Simulations: {summary.simulations:,}")
    print(f"Target Balance: {format_currency(target_balance)}")
    print(f"Average Final Balance: {format_currency(summary.average_final_balance)}")
    print(f"Median Final Balance: {format_currency(summary.median_final_balance)}")
    print(f"Standard Deviation: {format_currency(summary.standard_deviation)}")
    print(f"10th Percentile: {format_currency(summary.percentile_10)}")
    print(f"25th Percentile: {format_currency(summary.percentile_25)}")
    print(f"75th Percentile: {format_currency(summary.percentile_75)}")
    print(f"90th Percentile: {format_currency(summary.percentile_90)}")
    print(
        "Probability of Reaching Target: "
        f"{format_percentage(summary.probability_reaching_target)}"
    )
    print("=" * 70)


def export_projection_to_csv(
    projections: List[YearlyProjection],
    file_path: Path,
) -> None:
    """Exports deterministic projection results to a CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=[
                "year",
                "starting_balance",
                "contribution",
                "investment_return",
                "ending_balance",
                "inflation_adjusted_balance",
            ],
        )
        writer.writeheader()

        for row in projections:
            writer.writerow(
                {
                    "year": row.year,
                    "starting_balance": round(row.starting_balance, 2),
                    "contribution": round(row.contribution, 2),
                    "investment_return": round(row.investment_return, 2),
                    "ending_balance": round(row.ending_balance, 2),
                    "inflation_adjusted_balance": round(row.inflation_adjusted_balance, 2),
                }
            )


def export_simulation_summary_to_csv(
    summary: SimulationSummary,
    target_balance: float,
    file_path: Path,
) -> None:
    """Exports Monte Carlo simulation summary results to a CSV file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    summary_data: Dict[str, float] = {
        "simulations": summary.simulations,
        "target_balance": target_balance,
        "average_final_balance": round(summary.average_final_balance, 2),
        "median_final_balance": round(summary.median_final_balance, 2),
        "standard_deviation": round(summary.standard_deviation, 2),
        "percentile_10": round(summary.percentile_10, 2),
        "percentile_25": round(summary.percentile_25, 2),
        "percentile_75": round(summary.percentile_75, 2),
        "percentile_90": round(summary.percentile_90, 2),
        "probability_reaching_target": round(summary.probability_reaching_target, 4),
    }

    with file_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(summary_data.keys()))
        writer.writeheader()
        writer.writerow(summary_data)


def main() -> None:
    """Runs the compound interest scenario simulation workflow."""
    assumptions = collect_investment_assumptions()
    projection = build_deterministic_projection(assumptions)
    simulation_results = run_monte_carlo_simulation(assumptions)
    simulation_summary = summarize_simulation_results(
        simulation_results,
        assumptions.target_balance,
    )

    print_deterministic_projection(projection)
    print_simulation_summary(simulation_summary, assumptions.target_balance)

    if get_yes_no("\nExport projection and simulation summary to CSV? Y/N: "):
        export_projection_to_csv(
            projection,
            Path("outputs/compound_interest_projection.csv"),
        )
        export_simulation_summary_to_csv(
            simulation_summary,
            assumptions.target_balance,
            Path("outputs/compound_interest_simulation_summary.csv"),
        )
        print("\nFiles exported to the outputs folder.")


if __name__ == "__main__":
    main()
