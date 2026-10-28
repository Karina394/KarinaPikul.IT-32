import math
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

print("Karina Pikul, IT-32")

file_path = Path(__file__).parent / "data" / "expenses.csv"

if not file_path.is_file():
    print(f"error: file not found: {file_path}", file=sys.stderr)
    sys.exit(1)

expenses = defaultdict(list)

with file_path.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(";")

        try:
            if len(parts) != 4:
                raise ValueError("expected 4 fields")

            expense_date = date.fromisoformat(parts[0])
            amount = float(parts[2])

            if not math.isfinite(amount) or amount < 0:
                raise ValueError("invalid amount")

            expenses[expense_date].append(amount)

        except ValueError as error:
            print(
                f"warning: line {line_number}: {error}",
                file=sys.stderr
            )

if not expenses:
    print("error: no valid expenses", file=sys.stderr)
    sys.exit(1)

first_date = min(expenses)
last_date = max(expenses)
days_count = (last_date - first_date).days + 1

dates = [
    first_date + timedelta(days=i)
    for i in range(days_count)
]

daily_totals = {
    day: math.fsum(expenses.get(day, []))
    for day in dates
}

print(
    f"period: {first_date:%d.%m.%Y} ({first_date:%A}) - "
    f"{last_date:%d.%m.%Y} ({last_date:%A}), "
    f"{days_count} days"
)

print("\nweekday      total")

for weekday in range(7):
    total = math.fsum(
        amount
        for day, amount in daily_totals.items()
        if day.weekday() == weekday
    )
    weekday_name = date(2026, 1, 5 + weekday).strftime("%A")
    print(f"{weekday_name:<12} {total:8.2f}")

total = math.fsum(daily_totals.values())
average = total / days_count

variance = math.fsum(
    (amount - average) ** 2
    for amount in daily_totals.values()
) / days_count

std_dev = math.sqrt(variance)

top_day = max(daily_totals, key=daily_totals.get)
no_spend_days = sum(
    amount == 0 for amount in daily_totals.values()
)

month_start = last_date.replace(day=1)

if last_date.month == 12:
    next_month = date(last_date.year + 1, 1, 1)
else:
    next_month = date(last_date.year, last_date.month + 1, 1)

days_in_month = (next_month - month_start).days
days_left = days_in_month - last_date.day
forecast = average * days_in_month

print(f"\ntotal:        {total:.2f}")
print(f"per day:      {average:.2f} +- {std_dev:.2f}")
print(
    f"top day:      {top_day:%d.%m.%Y} "
    f"({top_day:%A}), {daily_totals[top_day]:.2f}"
)
print(f"no-spend days: {no_spend_days}")
print(
    f"days in {last_date:%B}: {days_in_month}, "
    f"left after {last_date:%d.%m}: {days_left}"
)
print(f"month forecast: {forecast:.2f}")
