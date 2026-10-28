from pathlib import Path
from collections import defaultdict
from tabulate import tabulate

print("Karina Pikul, IT-32")

file_path = Path(__file__).parent / "data" / "expenses.csv"
expenses = defaultdict(list)

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        date, category, amount, note = line.split(";")
        expenses[category].append(float(amount))

table = []
total_count = 0
total_amount = 0

for category, amounts in sorted(expenses.items()):
    count = len(amounts)
    total = sum(amounts)

    table.append([category, count, f"{total:.2f}"])
    total_count += count
    total_amount += total

table.append(["TOTAL", total_count, f"{total_amount:.2f}"])

print(tabulate(
    table,
    headers=["category", "count", "total"],
    tablefmt="github"
))
