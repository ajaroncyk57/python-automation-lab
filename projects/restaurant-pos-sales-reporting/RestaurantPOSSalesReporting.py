"""
Restaurant POS Sales Reporting

A command-line Python point-of-sale (POS) and sales reporting tool for capturing
customer orders, calculating order totals, and producing an end-of-day sales report.

Author: Andrew Jaroncyk
Created: 2019-09-27
Rebuilt: 2026-04-24
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MenuItem:
    """Represents a menu item available for purchase."""

    code: str
    name: str
    category: str
    price: float


@dataclass
class OrderLine:
    """Represents one selected item within an order."""

    item: MenuItem
    quantity: int = 1

    @property
    def line_total(self) -> float:
        """Calculates the total value of the order line."""
        return self.item.price * self.quantity


@dataclass
class Order:
    """Represents a customer order."""

    order_id: int
    order_lines: List[OrderLine]

    @property
    def order_total(self) -> float:
        """Calculates the total value of the order."""
        return sum(line.line_total for line in self.order_lines)


MENU: Dict[str, MenuItem] = {
    "B": MenuItem("B", "Beef Burger", "Burger", 5.75),
    "Y": MenuItem("Y", "Beyond Beef Burger", "Burger", 6.25),
    "D": MenuItem("D", "Double Patty Upgrade", "Upgrade", 2.00),
    "T": MenuItem("T", "Triple Patty Upgrade", "Upgrade", 3.50),
    "C": MenuItem("C", "Cheese", "Topping", 0.50),
    "BA": MenuItem("BA", "Bacon", "Topping", 1.25),
    "A": MenuItem("A", "Avocado", "Topping", 0.75),
    "CH": MenuItem("CH", "Chili", "Topping", 2.50),
    "F": MenuItem("F", "Fries", "Side", 2.00),
    "R": MenuItem("R", "Onion Rings", "Side", 2.25),
}


def format_currency(value: float) -> str:
    """Formats a numeric value as currency."""
    return f"${value:,.2f}"


def get_choice(prompt: str, valid_choices: List[str]) -> str:
    """Safely collects a valid menu choice from the user."""
    normalized_choices = [choice.upper() for choice in valid_choices]

    while True:
        choice = input(prompt).strip().upper()

        if choice in normalized_choices:
            return choice

        print(f"Please enter one of the following: {', '.join(normalized_choices)}")


def get_yes_no(prompt: str) -> bool:
    """Collects a yes/no response from the user."""
    choice = get_choice(prompt, ["Y", "N"])
    return choice == "Y"


def add_item(order_lines: List[OrderLine], item_code: str) -> None:
    """Adds a menu item to the current order."""
    order_lines.append(OrderLine(item=MENU[item_code]))


def capture_order(order_id: int) -> Order:
    """Captures a customer order through the command line."""
    order_lines: List[OrderLine] = []

    print("\nNew Customer Order")
    print("-" * 50)

    burger_choice = get_choice(
        "Choose Burger: Beef (B) or Beyond Beef (Y): ",
        ["B", "Y"],
    )
    add_item(order_lines, burger_choice)

    patty_choice = get_choice(
        "Upgrade Patty? Double (D), Triple (T), or None (N): ",
        ["D", "T", "N"],
    )

    if patty_choice != "N":
        add_item(order_lines, patty_choice)

    if get_yes_no("Add Toppings? Y/N: "):
        if get_yes_no("Add Cheese? Y/N: "):
            add_item(order_lines, "C")

        if get_yes_no("Add Bacon? Y/N: "):
            add_item(order_lines, "BA")

        if get_yes_no("Add Avocado? Y/N: "):
            add_item(order_lines, "A")

        if get_yes_no("Add Chili? Y/N: "):
            add_item(order_lines, "CH")

    side_choice = get_choice(
        "Add a Side? Fries (F), Onion Rings (R), or None (N): ",
        ["F", "R", "N"],
    )

    if side_choice != "N":
        add_item(order_lines, side_choice)

    return Order(order_id=order_id, order_lines=order_lines)


def print_receipt(order: Order) -> None:
    """Prints a receipt for a customer order."""
    print("\nOrder Receipt")
    print("=" * 50)
    print(f"Order ID: {order.order_id}")
    print("-" * 50)

    for line in order.order_lines:
        print(
            f"{line.item.name:<30} "
            f"x{line.quantity:<3} "
            f"{format_currency(line.line_total):>10}"
        )

    print("-" * 50)
    print(f"{'Order Total:':<35}{format_currency(order.order_total):>10}")
    print("=" * 50)


def summarize_item_sales(orders: List[Order]) -> Dict[str, Dict[str, float]]:
    """Summarizes quantity and revenue by menu item."""
    sales_summary: Dict[str, Dict[str, float]] = {}

    for order in orders:
        for line in order.order_lines:
            item_name = line.item.name

            if item_name not in sales_summary:
                sales_summary[item_name] = {
                    "quantity": 0,
                    "revenue": 0.0,
                }

            sales_summary[item_name]["quantity"] += line.quantity
            sales_summary[item_name]["revenue"] += line.line_total

    return sales_summary


def summarize_category_sales(orders: List[Order]) -> Dict[str, float]:
    """Summarizes revenue by menu category."""
    category_summary: Dict[str, float] = {}

    for order in orders:
        for line in order.order_lines:
            category = line.item.category

            if category not in category_summary:
                category_summary[category] = 0.0

            category_summary[category] += line.line_total

    return category_summary


def print_end_of_day_report(orders: List[Order]) -> None:
    """Prints an end-of-day sales report."""
    print("\n")
    print("=" * 70)
    print("EOD Sales Report")
    print("=" * 70)

    if not orders:
        print("No orders were captured.")
        print("=" * 70)
        return

    total_orders = len(orders)
    total_revenue = sum(order.order_total for order in orders)
    average_order_value = total_revenue / total_orders

    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: {format_currency(total_revenue)}")
    print(f"Average Order Value (AOV): {format_currency(average_order_value)}")

    print("\nItem Sales")
    print("-" * 70)
    print(f"{'Item':<30}{'Quantity':>10}{'Revenue':>15}")

    item_sales = summarize_item_sales(orders)

    for item_name, metrics in sorted(item_sales.items()):
        print(
            f"{item_name:<30}"
            f"{int(metrics['quantity']):>10}"
            f"{format_currency(metrics['revenue']):>15}"
        )

    print("\nCategory Revenue")
    print("-" * 70)
    print(f"{'Category':<30}{'Revenue':>15}")

    category_sales = summarize_category_sales(orders)

    for category, revenue in sorted(category_sales.items()):
        print(f"{category:<30}{format_currency(revenue):>15}")

    print("=" * 70)


def main() -> None:
    """Runs the restaurant POS sales reporting workflow."""
    orders: List[Order] = []
    next_order_id = 1

    print("Restaurant POS Sales Reporting")
    print("=" * 50)

    while True:
        order = capture_order(next_order_id)
        orders.append(order)
        print_receipt(order)

        next_order_id += 1

        continue_orders = get_yes_no("\nStart another Order? Y/N: ")

        if not continue_orders:
            break

    print_end_of_day_report(orders)


if __name__ == "__main__":
    main()
