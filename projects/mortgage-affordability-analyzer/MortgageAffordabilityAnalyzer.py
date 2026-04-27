"""
Mortgage Affordability Analyzer

A command-line Python tool for evaluating home affordability using mortgage
payment calculations, debt-to-income ratios, monthly budget assumptions, and
stress-test scenarios.

This project expands an early mortgage/budget calculator into a more practical
personal finance analytics tool.

Author: Andrew Jaroncyk
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MortgageAssumptions:
    """Stores mortgage-related assumptions."""

    purchase_price: float
    down_payment: float
    annual_interest_rate: float
    mortgage_term_years: int
    annual_property_tax_rate: float
    annual_home_insurance: float
    monthly_hoa_fee: float
    monthly_pmi: float

    @property
    def loan_amount(self) -> float:
        """Calculates the mortgage principal after down payment."""
        return self.purchase_price - self.down_payment

    @property
    def down_payment_percentage(self) -> float:
        """Calculates down payment as a percentage of purchase price."""
        if self.purchase_price == 0:
            return 0.0
        return self.down_payment / self.purchase_price

    @property
    def monthly_interest_rate(self) -> float:
        """Converts annual mortgage interest rate to monthly rate."""
        return self.annual_interest_rate / 12

    @property
    def number_of_payments(self) -> int:
        """Calculates total number of mortgage payments."""
        return self.mortgage_term_years * 12

    @property
    def monthly_property_tax(self) -> float:
        """Calculates estimated monthly property tax."""
        return (self.purchase_price * self.annual_property_tax_rate) / 12

    @property
    def monthly_home_insurance(self) -> float:
        """Calculates monthly homeowners insurance."""
        return self.annual_home_insurance / 12


@dataclass
class BudgetAssumptions:
    """Stores household income and expense assumptions."""

    annual_gross_income: float
    monthly_food_expense: float
    monthly_utilities: float
    monthly_transportation: float
    monthly_debt_payments: float
    monthly_other_expenses: float

    @property
    def monthly_gross_income(self) -> float:
        """Calculates gross monthly income."""
        return self.annual_gross_income / 12

    @property
    def non_housing_expenses(self) -> float:
        """Calculates monthly expenses excluding housing costs."""
        return (
            self.monthly_food_expense
            + self.monthly_utilities
            + self.monthly_transportation
            + self.monthly_debt_payments
            + self.monthly_other_expenses
        )


@dataclass
class AffordabilityResult:
    """Stores mortgage affordability calculation outputs."""

    principal_and_interest: float
    total_monthly_housing_cost: float
    total_monthly_expenses: float
    monthly_cash_leftover: float
    front_end_dti: float
    back_end_dti: float
    affordable_housing_limit: float
    total_interest_paid: float
    total_payment_over_loan: float
    affordability_status: str


def format_currency(value: float) -> str:
    """Formats a numeric value as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Formats a decimal value as a percentage."""
    return f"{value * 100:.2f}%"


def get_float_input(prompt: str, minimum: Optional[float] = None) -> float:
    """Safely collects numeric input from the user."""
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
    """Safely collects integer input from the user."""
    while True:
        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Please enter a value greater than or equal to {minimum}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")


def collect_mortgage_assumptions() -> MortgageAssumptions:
    """Collects mortgage assumptions from the user."""
    print("\nMortgage Inputs")
    print("-" * 50)

    purchase_price = get_float_input("Enter purchase price: $", minimum=1)
    down_payment = get_float_input("Enter down payment amount: $", minimum=0)

    while down_payment > purchase_price:
        print("Down payment cannot exceed purchase price.")
        down_payment = get_float_input("Enter down payment amount: $", minimum=0)

    annual_interest_rate = get_float_input(
        "Enter mortgage interest rate as a decimal, e.g. 0.065 for 6.5%: ",
        minimum=0,
    )

    mortgage_term_years = get_int_input("Enter mortgage term in years: ", minimum=1)

    annual_property_tax_rate = get_float_input(
        "Enter annual property tax rate as a decimal, e.g. 0.012 for 1.2%: ",
        minimum=0,
    )

    annual_home_insurance = get_float_input(
        "Enter estimated annual homeowners insurance: $",
        minimum=0,
    )

    monthly_hoa_fee = get_float_input("Enter monthly HOA/condo fee: $", minimum=0)
    monthly_pmi = get_float_input("Enter monthly PMI, if applicable: $", minimum=0)

    return MortgageAssumptions(
        purchase_price=purchase_price,
        down_payment=down_payment,
        annual_interest_rate=annual_interest_rate,
        mortgage_term_years=mortgage_term_years,
        annual_property_tax_rate=annual_property_tax_rate,
        annual_home_insurance=annual_home_insurance,
        monthly_hoa_fee=monthly_hoa_fee,
        monthly_pmi=monthly_pmi,
    )


def collect_budget_assumptions() -> BudgetAssumptions:
    """Collects monthly income and expense assumptions from the user."""
    print("\nBudget Inputs")
    print("-" * 50)

    annual_gross_income = get_float_input("Enter annual gross income: $", minimum=0)
    monthly_food_expense = get_float_input("Enter monthly food expense: $", minimum=0)
    monthly_utilities = get_float_input("Enter monthly utilities: $", minimum=0)
    monthly_transportation = get_float_input("Enter monthly transportation/car expense: $", minimum=0)
    monthly_debt_payments = get_float_input("Enter monthly debt payments: $", minimum=0)
    monthly_other_expenses = get_float_input("Enter other monthly expenses: $", minimum=0)

    return BudgetAssumptions(
        annual_gross_income=annual_gross_income,
        monthly_food_expense=monthly_food_expense,
        monthly_utilities=monthly_utilities,
        monthly_transportation=monthly_transportation,
        monthly_debt_payments=monthly_debt_payments,
        monthly_other_expenses=monthly_other_expenses,
    )


def calculate_monthly_principal_and_interest(mortgage: MortgageAssumptions) -> float:
    """Calculates monthly mortgage principal and interest payment."""
    loan_amount = mortgage.loan_amount
    monthly_rate = mortgage.monthly_interest_rate
    number_of_payments = mortgage.number_of_payments

    if loan_amount <= 0:
        return 0.0

    if monthly_rate == 0:
        return loan_amount / number_of_payments

    return loan_amount * (
        monthly_rate * (1 + monthly_rate) ** number_of_payments
    ) / ((1 + monthly_rate) ** number_of_payments - 1)


def calculate_total_monthly_housing_cost(mortgage: MortgageAssumptions) -> float:
    """Calculates estimated total monthly housing cost."""
    principal_and_interest = calculate_monthly_principal_and_interest(mortgage)

    return (
        principal_and_interest
        + mortgage.monthly_property_tax
        + mortgage.monthly_home_insurance
        + mortgage.monthly_hoa_fee
        + mortgage.monthly_pmi
    )


def calculate_affordability_status(front_end_dti: float, back_end_dti: float) -> str:
    """Classifies affordability using common DTI thresholds."""
    if front_end_dti <= 0.28 and back_end_dti <= 0.36:
        return "Strong Fit: Housing and total debt ratios are within traditional affordability guidelines."

    if front_end_dti <= 0.30 and back_end_dti <= 0.43:
        return "Moderate Fit: Potentially affordable, but the budget is tighter and should be stress-tested."

    return "High Risk: Housing or total debt ratios exceed common affordability guidelines."


def analyze_affordability(
    mortgage: MortgageAssumptions,
    budget: BudgetAssumptions,
    housing_limit_percentage: float = 0.30,
) -> AffordabilityResult:
    """Calculates mortgage affordability metrics."""
    principal_and_interest = calculate_monthly_principal_and_interest(mortgage)
    total_monthly_housing_cost = calculate_total_monthly_housing_cost(mortgage)
    total_monthly_expenses = total_monthly_housing_cost + budget.non_housing_expenses
    monthly_cash_leftover = budget.monthly_gross_income - total_monthly_expenses

    front_end_dti = total_monthly_housing_cost / budget.monthly_gross_income if budget.monthly_gross_income else 0
    back_end_dti = (
        total_monthly_housing_cost + budget.monthly_debt_payments
    ) / budget.monthly_gross_income if budget.monthly_gross_income else 0

    affordable_housing_limit = budget.monthly_gross_income * housing_limit_percentage
    total_payment_over_loan = principal_and_interest * mortgage.number_of_payments
    total_interest_paid = total_payment_over_loan - mortgage.loan_amount
    affordability_status = calculate_affordability_status(front_end_dti, back_end_dti)

    return AffordabilityResult(
        principal_and_interest=principal_and_interest,
        total_monthly_housing_cost=total_monthly_housing_cost,
        total_monthly_expenses=total_monthly_expenses,
        monthly_cash_leftover=monthly_cash_leftover,
        front_end_dti=front_end_dti,
        back_end_dti=back_end_dti,
        affordable_housing_limit=affordable_housing_limit,
        total_interest_paid=total_interest_paid,
        total_payment_over_loan=total_payment_over_loan,
        affordability_status=affordability_status,
    )


def build_rate_stress_test(
    mortgage: MortgageAssumptions,
    budget: BudgetAssumptions,
    rate_changes: List[float],
) -> List[Dict[str, float]]:
    """Builds interest-rate stress-test scenarios."""
    scenarios: List[Dict[str, float]] = []

    for rate_change in rate_changes:
        stressed_mortgage = MortgageAssumptions(
            purchase_price=mortgage.purchase_price,
            down_payment=mortgage.down_payment,
            annual_interest_rate=max(mortgage.annual_interest_rate + rate_change, 0),
            mortgage_term_years=mortgage.mortgage_term_years,
            annual_property_tax_rate=mortgage.annual_property_tax_rate,
            annual_home_insurance=mortgage.annual_home_insurance,
            monthly_hoa_fee=mortgage.monthly_hoa_fee,
            monthly_pmi=mortgage.monthly_pmi,
        )
        result = analyze_affordability(stressed_mortgage, budget)

        scenarios.append(
            {
                "rate_change": rate_change,
                "interest_rate": stressed_mortgage.annual_interest_rate,
                "principal_and_interest": result.principal_and_interest,
                "total_monthly_housing_cost": result.total_monthly_housing_cost,
                "front_end_dti": result.front_end_dti,
                "monthly_cash_leftover": result.monthly_cash_leftover,
            }
        )

    return scenarios


def estimate_max_purchase_price(
    budget: BudgetAssumptions,
    mortgage: MortgageAssumptions,
    housing_limit_percentage: float = 0.30,
    search_min: float = 50_000,
    search_max: float = 2_000_000,
    tolerance: float = 100,
) -> float:
    """Estimates max purchase price based on a target housing-cost percentage."""
    target_housing_cost = budget.monthly_gross_income * housing_limit_percentage
    down_payment_ratio = mortgage.down_payment_percentage

    lower = search_min
    upper = search_max
    best_price = lower

    while upper - lower > tolerance:
        midpoint = (lower + upper) / 2
        test_down_payment = midpoint * down_payment_ratio

        test_mortgage = MortgageAssumptions(
            purchase_price=midpoint,
            down_payment=test_down_payment,
            annual_interest_rate=mortgage.annual_interest_rate,
            mortgage_term_years=mortgage.mortgage_term_years,
            annual_property_tax_rate=mortgage.annual_property_tax_rate,
            annual_home_insurance=mortgage.annual_home_insurance,
            monthly_hoa_fee=mortgage.monthly_hoa_fee,
            monthly_pmi=mortgage.monthly_pmi,
        )

        housing_cost = calculate_total_monthly_housing_cost(test_mortgage)

        if housing_cost <= target_housing_cost:
            best_price = midpoint
            lower = midpoint
        else:
            upper = midpoint

    return best_price


def print_affordability_report(
    mortgage: MortgageAssumptions,
    budget: BudgetAssumptions,
    result: AffordabilityResult,
) -> None:
    """Prints a full mortgage affordability report."""
    print("\n")
    print("=" * 80)
    print("Mortgage Affordability Report")
    print("=" * 80)

    print("\nMortgage Summary")
    print("-" * 80)
    print(f"Purchase Price: {format_currency(mortgage.purchase_price)}")
    print(f"Down Payment: {format_currency(mortgage.down_payment)}")
    print(f"Down Payment Percentage: {format_percentage(mortgage.down_payment_percentage)}")
    print(f"Loan Amount: {format_currency(mortgage.loan_amount)}")
    print(f"Mortgage Term: {mortgage.mortgage_term_years} years")
    print(f"Interest Rate: {format_percentage(mortgage.annual_interest_rate)}")

    print("\nMonthly Housing Cost")
    print("-" * 80)
    print(f"Principal & Interest: {format_currency(result.principal_and_interest)}")
    print(f"Property Tax: {format_currency(mortgage.monthly_property_tax)}")
    print(f"Homeowners Insurance: {format_currency(mortgage.monthly_home_insurance)}")
    print(f"HOA / Condo Fee: {format_currency(mortgage.monthly_hoa_fee)}")
    print(f"PMI: {format_currency(mortgage.monthly_pmi)}")
    print(f"Total Monthly Housing Cost: {format_currency(result.total_monthly_housing_cost)}")

    print("\nBudget Summary")
    print("-" * 80)
    print(f"Monthly Gross Income: {format_currency(budget.monthly_gross_income)}")
    print(f"Non-Housing Monthly Expenses: {format_currency(budget.non_housing_expenses)}")
    print(f"Total Monthly Expenses Including Housing: {format_currency(result.total_monthly_expenses)}")
    print(f"Estimated Monthly Cash Leftover: {format_currency(result.monthly_cash_leftover)}")
    print(f"30% Housing Cost Benchmark: {format_currency(result.affordable_housing_limit)}")

    print("\nAffordability Metrics")
    print("-" * 80)
    print(f"Front-End DTI: {format_percentage(result.front_end_dti)}")
    print(f"Back-End DTI: {format_percentage(result.back_end_dti)}")
    print(f"Total Principal & Interest Paid: {format_currency(result.total_payment_over_loan)}")
    print(f"Total Interest Paid: {format_currency(result.total_interest_paid)}")

    print("\nRecommendation")
    print("-" * 80)
    print(result.affordability_status)
    print("=" * 80)


def print_stress_test_report(scenarios: List[Dict[str, float]]) -> None:
    """Prints rate stress-test results."""
    print("\nInterest Rate Stress Test")
    print("=" * 90)
    print(
        f"{'Rate Change':<14}"
        f"{'Rate':>10}"
        f"{'P&I':>15}"
        f"{'Housing Cost':>18}"
        f"{'Front DTI':>14}"
        f"{'Cash Left':>16}"
    )
    print("-" * 90)

    for scenario in scenarios:
        print(
            f"{format_percentage(scenario['rate_change']):<14}"
            f"{format_percentage(scenario['interest_rate']):>10}"
            f"{format_currency(scenario['principal_and_interest']):>15}"
            f"{format_currency(scenario['total_monthly_housing_cost']):>18}"
            f"{format_percentage(scenario['front_end_dti']):>14}"
            f"{format_currency(scenario['monthly_cash_leftover']):>16}"
        )

    print("=" * 90)


def main() -> None:
    """Runs the mortgage affordability analysis workflow."""
    print("Mortgage Affordability Analyzer")
    print("=" * 50)

    mortgage = collect_mortgage_assumptions()
    budget = collect_budget_assumptions()
    result = analyze_affordability(mortgage, budget)
    stress_test = build_rate_stress_test(
        mortgage,
        budget,
        rate_changes=[-0.01, -0.005, 0.0, 0.005, 0.01, 0.02],
    )
    max_purchase_price = estimate_max_purchase_price(budget, mortgage)

    print_affordability_report(mortgage, budget, result)
    print_stress_test_report(stress_test)
    print(
        "\nEstimated Max Purchase Price at 30% Housing Benchmark: "
        f"{format_currency(max_purchase_price)}"
    )


if __name__ == "__main__":
    main()
