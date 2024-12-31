import argparse
import importlib.util
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


def load_expected_solutions(filename):
    solutions = {}
    with open(filename) as f:
        for line in f:
            day, part, value = line.strip().split()
            solutions[(int(day), int(part))] = value
    return solutions

def load_challenge_solution(day):
    """Dynamically load a solution module for the given day."""
    module_name = f"day{day:02d}"
    module_path = os.path.join(f"{day:02d}", f"{module_name}.py")

    if not os.path.exists(module_path):
        print(f"Error:  Loading solution module for day {day} from {module_path}...")
        raise FileNotFoundError(f"Solution module for day {day} not found.")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_challenge(day, part, expected_solutions, details=False):
    function_name = f"day{day}Part{part}"
    try:
        module = load_challenge_solution(day)
        function = getattr(module, function_name)
        start_time = time.time()
        result, description = function("input.txt")
        end_time = time.time()
        duration = end_time - start_time
        expected_value = expected_solutions.get((day, part))
        if str(result) == str(expected_value):
            print(f"Day {day} Part {part}: PASS", end="")
        else:
            print(f"Day {day} Part {part}: FAIL (Expected: [{expected_value}], Got: [{result}])", end="")
        if details:
            print(f" {description} {result}", end="")
        print(f" ({duration:.6f} seconds)")
    except (ImportError, AttributeError) as e:
        print(f"Day {day} Part {part}: ERROR ({e})")

def main():
    parser = argparse.ArgumentParser(description="Run AoC challenges and compare results with expected values.")
    parser.add_argument("--days", type=int, nargs="*", help="Specify which days to run (e.g., --days 1 2 3).")
    parser.add_argument("--parts", type=int, nargs="*", help="Specify which parts to run (e.g., --parts 1 2).")
    parser.add_argument("--all", action="store_true", help="Run all challenges.")
    parser.add_argument("--details", action="store_true", help="Print description and result for each challenge.")
    args = parser.parse_args()

    expected_solutions = load_expected_solutions("solutions.txt")

    days = args.days if args.days else range(1, 26)
    parts = args.parts if args.parts else [1, 2]
    details = args.details

    for day in days:
        for part in parts:
            run_challenge(day, part, expected_solutions, details)

if __name__ == "__main__":
    main()


