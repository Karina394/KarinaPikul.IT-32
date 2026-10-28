import math
import sys
from datetime import datetime
from pathlib import Path

print("Karina Pikul, IT-32")

args = sys.argv[1:]
dry_run = False

if args and args[0] == "--dry-run":
    dry_run = True
    args = args[1:]

if len(args) != 1:
    print("Usage: python3 task3.py [--dry-run] <dir>", file=sys.stderr)
    sys.exit(2)

target = Path(args[0]).expanduser()

if not target.exists() or not target.is_dir():
    print(f"error: directory not found: {target}", file=sys.stderr)
    sys.exit(1)

items = []

for path in target.iterdir():
    if not path.is_file():
        continue

    stat = path.stat()
    modified = datetime.fromtimestamp(stat.st_mtime)
    month = modified.strftime("%Y-%m")
    destination = target / month / path.name

    size = stat.st_size

    if size == 0:
        unit_index = 0
    else:
        unit_index = min(int(math.log(size, 1024)), 3)

    units = ("B", "KB", "MB", "GB")
    readable_size = size / (1024 ** unit_index)
    size_text = f"{readable_size:.2f} {units[unit_index]}"

    items.append((
        stat.st_mtime,
        path,
        destination,
        modified,
        month,
        size_text
    ))

items.sort(key=lambda item: item[0])

if not items:
    print("No files found.")
    sys.exit(0)

print("\nFiles to organize:")

for _, path, destination, modified, month, size_text in items:
    print(
        f"{path.name:<25} {size_text:>12}  "
        f"{modified:%d.%m.%Y %H:%M}  -> {month}/"
    )

conflicts = [
    destination
    for _, _, destination, _, _, _ in items
    if destination.exists()
]

if conflicts:
    for destination in conflicts:
        print(
            f"error: destination already exists: {destination}",
            file=sys.stderr
        )
    sys.exit(1)

folder_count = len({item[4] for item in items})

if dry_run:
    print(
        f"\n{len(items)} files, {folder_count} folders "
        "(dry run, nothing moved)"
    )
    sys.exit(0)

for _, path, destination, _, _, _ in items:
    destination.parent.mkdir(parents=True, exist_ok=True)
    path.rename(destination)

script_dir = Path(__file__).parent
reports_dir = script_dir / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
report_path = reports_dir / f"organize_{timestamp}.txt"

report_lines = [
    "Karina Pikul, IT-32",
    f"Organized directory: {target}",
    f"Files moved: {len(items)}",
    f"Folders used: {folder_count}",
    "",
]

for _, path, destination, modified, month, size_text in items:
    report_lines.append(
        f"{path.name} | {size_text} | "
        f"{modified:%d.%m.%Y %H:%M} | {month}/"
    )

report_path.write_text(
    "\n".join(report_lines) + "\n",
    encoding="utf-8"
)

print(f"\n{len(items)} files, {folder_count} folders")
print(f"Report saved: {report_path}")
