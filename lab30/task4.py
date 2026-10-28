import csv
import math
import random
import sys
from datetime import datetime
from pathlib import Path

print("Karina Pikul, IT-32")

YEAR = 2009
random.seed(YEAR)

script_dir = Path(__file__).parent
results_dir = script_dir / "results"
history_file = results_dir / "history.csv"

root = random.randint(5, 20)
factorial_n = random.randint(3, 6)
a = random.randint(24, 90)
b = random.randint(24, 90)
comb_n = random.randint(5, 9)
comb_k = random.randint(2, comb_n - 1)
percent = random.choice([5, 10, 15, 20])
amount = random.choice([100, 200, 260, 400, 500])

questions = [
    (f"sqrt({root * root})", math.isqrt(root * root)),
    (f"{factorial_n}!", math.factorial(factorial_n)),
    (f"gcd({a}, {b})", math.gcd(a, b)),
    (f"C({comb_n}, {comb_k})", math.comb(comb_n, comb_k)),
    (f"{percent}% of {amount}", amount * percent // 100),
]

score = 0
start = datetime.now()

for number, (question, correct_answer) in enumerate(questions, start=1):
    answer = input(f"{number}. {question} = ").strip()

    try:
        user_answer = int(answer)
    except ValueError:
        user_answer = None

    if user_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Incorrect. Correct answer: {correct_answer}")

elapsed = (datetime.now() - start).total_seconds()

results_dir.mkdir(parents=True, exist_ok=True)
new_file = not history_file.exists()

try:
    with history_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        if new_file:
            writer.writerow(["datetime", "score", "seconds"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score,
            f"{elapsed:.2f}"
        ])

    history = []

    with history_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")

        for row in reader:
            try:
                history.append({
                    "datetime": row["datetime"],
                    "score": int(row["score"]),
                    "seconds": float(row["seconds"])
                })
            except (ValueError, KeyError, TypeError):
                print("warning: invalid history record", file=sys.stderr)

except OSError as error:
    print(f"error: cannot work with history: {error}", file=sys.stderr)
    sys.exit(1)

print(f"\nResult: {score}/5")
print(f"Time: {elapsed:.2f} seconds")
print(f"Attempts: {len(history)}")

best = max(history, key=lambda item: (item["score"], -item["seconds"]))

print(
    f"Best: {best['score']}/5 in {best['seconds']:.2f} seconds "
    f"({best['datetime']})"
)
