# -*- coding: utf-8 -*-
"""
Capital Budgeting Investment Analysis
Created: 2019-11-05

A Command-Line Python tool for evaluating Investment Projects using common Capital Budgeting Metrics, including:
- Net Present Value (NPV)
- Internal Rate of Return (IRR)
- Return on Investment (ROI)
- Payback Period
- Profitability Index

Author: Andrew Jaroncyk

"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ProjectAssumptions:
    """"Stores assumptions used to evaluate Investment Project"""
    
    project_name: str
    initial_investment: float
    annual_cash_inflow: float
    annual_cash_outflow: float
    project_lifetime_years: int
    required_rate_of_return: float
    
    @property
    def annual_net_cash_flow(self) -> float:
        """Calculates Annual Net Cash Flow"""
        return self.annual_cash_inflow - self.annual_cash_outflow
    
    @property
    def cash_flows(self) -> List[float]:
        """Returns full project Cash Flow Series"""
        return [-self.initial_investment] + [
            self.annual_net_cash_flow for _ in range(self.project_lifetime_years)
        ]
        

def get_float_input(prompt: str, minimum: Optional[float] = None) -> float:
    """Safely collects numeric input from User"""
    while True:
        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Please enter a value greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Enter a valid number")
            
            
def get_int_input(prompt: str, minimum: Optional[int] = None) -> int:
    """Safely collects integer input from User"""
    while True:
        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Enter a value greater than or equal to {minimum}")
                continue

            return value

        except ValueError:
            print("Enter a valid whole number")
        
              
def collect_project_assumptions() -> ProjectAssumptions:
    """Collects Project Assumptions from User"""

    print("\nCapital Budgeting Investment Analysis")
    print("-" * 45)

    project_name = input("Enter project name: ").strip()

    if not project_name:
        project_name = "Unnamed Project"

    initial_investment = get_float_input(
        "Enter initial investment amount: $",
        minimum=0,
    )

    annual_cash_inflow = get_float_input(
        "Enter expected annual cash inflow: $",
        minimum=0,
    )

    annual_cash_outflow = get_float_input(
        "Enter expected annual cash outflow: $",
        minimum=0,
    )

    project_lifetime_years = get_int_input(
        "Enter project lifetime in years: ",
        minimum=1,
    )

    required_rate_of_return = get_float_input(
        "Enter required rate of return as a decimal, e.g. 0.10 for 10%: ",
        minimum=0,
    )

    return ProjectAssumptions(
        project_name=project_name,
        initial_investment=initial_investment,
        annual_cash_inflow=annual_cash_inflow,
        annual_cash_outflow=annual_cash_outflow,
        project_lifetime_years=project_lifetime_years,
        required_rate_of_return=required_rate_of_return,
    )


def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """Calculates Net Present Value (NPV)"""
    
    return sum(
        cash_flow / ((1 + discount_rate) ** year)
        for year, cash_flow in enumerate(cash_flows)
    )
    
    
def calculate_roi(initial_investment: float, total_net_cash_flow: float) -> float:
    """Calculates Return on Investment (ROI)"""
    
    if initial_investment == 0:
        raise ValueError("Initial Investment cannot be zero when calculating ROI")

    return ((total_net_cash_flow - initial_investment) / initial_investment) * 100


def calculate_payback_period(
    initial_investment: float,
    annual_net_cash_flow: float,
) -> Optional[float]:
    
    if annual_net_cash_flow <= 0:
        return None
    
    return initial_investment / annual_net_cash_flow


def calculate_profitability_index(
    cash_flows: List[float],
    discount_rate: float,
) -> Optional[float]:
    """Calculates Payback Period in years"""
    
    initial_investment = abs(cash_flows[0])
    
    if initial_investment == 0:
        raise ValueError(
            "Initial Investment cannot be zero when calculating Profitability Index"
        )
        
    present_value_future_cash_flows = sum(
        cash_flow / ((1 + discount_rate) ** year)
        for year, cash_flow in enumerate(cash_flows[1:], start = 1)
    )
    
    return present_value_future_cash_flows / initial_investment


def calculate_irr(
    cash_flows: List[float],
    lower_bound: float = -0.99,
    upper_bound: float = 10.0,
    tolerance: float = 0.000001,
    max_iterations: int = 1000,
) -> Optional[float]:
    """
    Estimates Internal Rate of Return (IRR) using Bisection Method
    Returns `None` if Cash Flow Pattern does not produce solvable IRR within provided bounds
    """

    npv_lower = calculate_npv(cash_flows, lower_bound)
    npv_upper = calculate_npv(cash_flows, upper_bound)

    if npv_lower * npv_upper > 0:
        return None

    for _ in range(max_iterations):
        midpoint = (lower_bound + upper_bound) / 2
        npv_midpoint = calculate_npv(cash_flows, midpoint)

        if abs(npv_midpoint) < tolerance:
            return midpoint

        if npv_lower * npv_midpoint < 0:
            upper_bound = midpoint
            npv_upper = npv_midpoint
        else:
            lower_bound = midpoint
            npv_lower = npv_midpoint

    return midpoint


def get_recommendation(npv: float, irr: Optional[float], required_rate: float) -> str:
    """Returns Investment Recommendation based on NPV & IRR (optional)"""
    
    if npv > 0 and irr is not None and irr > required_rate:
        return "Accept: The Project has a positive NPV & IRR exceeds the Required Return"
    
    if npv > 0:
        return "Consider: The Project has a positive NPV, but IRR should be reviewed"
    
    if npv == 0:
        return "Neutral: The Project is approximately breakeven based on NPV"
    
    return "Reject: The Project has a negative NPV under the current assumptions"


def format_currency(value: float) -> str:
    """Formats numeric value as currency"""
    
    return f"${value:,.2f}"


def format_percentage(value: Optional[float]) -> str:
    """Formats decimal value as percentage"""
    
    if value is None:
        return "N/A"
    
    return f"{value * 100:.2f}%"


def print_project_report(project: ProjectAssumptions) -> None:
    """Prints Capital Budgeting Analysis Report"""
    
    cash_flows = project.cash_flows
    total_net_cash_flow = project.annual_net_cash_flow * project.project_lifetime_years
    
    npv = calculate_npv(cash_flows, project.required_rate_of_return)
    irr = calculate_irr(cash_flows)
    roi = calculate_roi(project.initial_investment, total_net_cash_flow)
    payback_period = calculate_payback_period(project.initial_investment, project.annual_net_cash_flow,)
    profitability_index = calculate_profitability_index(cash_flows, project.required_rate_of_return,)
    recommendation = get_recommendation(npv, irr, project.required_rate_of_return,)
    
    print("\n")
    print("=" * 70)
    print("Capital Budgeting Investment Report")
    print("=" * 70)
    
    print(f"Project Name: {project.project_name}")
    print(f"Initial Investment: {format_currency(project.initial_investment)}")
    print(f"Annual Cash Inflow: {format_currency(project.annual_cash_inflow)}")
    print(f"Annual Cash Outflow: {format_currency(project.annual_cash_outflow)}")
    print(f"Annual Net Cash Flow: {format_currency(project.annual_net_cash_flow)}")
    print(f"Project Lifetime: {project.project_lifetime_years} years")
    print(f"Required Rate of Return: {format_percentage(project.required_rate_of_return)}")


    print("\nProjected Cash Flows")
    print("-" * 70)

    for year, cash_flow in enumerate(cash_flows):
        print(f"Year {year}: {format_currency(cash_flow)}")

    print("\nInvestment Metrics")
    print("-" * 70)
    print(f"Net Present Value (NPV): {format_currency(npv)}")
    print(f"Internal Rate of Return (IRR): {format_percentage(irr)}")
    print(f"Return on Investment (ROI): {roi:.2f}%")

    if payback_period is None:
        print("Payback Period: N/A")
    else:
        print(f"Payback Period: {payback_period:.2f} years")

    print(f"Profitability Index: {profitability_index:.2f}")

    print("\nRecommendation")
    print("-" * 70)
    print(recommendation)
    print("=" * 70)


def main() -> None:
    """Runs Capital Budgeting Analysis Workflow"""

    while True:
        project = collect_project_assumptions()
        print_project_report(project)

        run_again = input("\nWould you like to analyze another project? (Y/N): ").strip().lower()

        if run_again != "y":
            print("\nThanks for using the Capital Budgeting Investment Analysis Tool!")
            break


if __name__ == "__main__":
    main()













    
