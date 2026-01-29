from math import pi
from time import time, strftime, gmtime
import json
from itertools import product
from component_formatting import format_resistor, format_capacitor


components = [
    {"label": "R1", "type": "R", "max_parts": 1},
    {"label": "R2", "type": "R", "max_parts": 1},
    {"label": "C1", "type": "C", "max_parts": 3},
]

equations = [
    {"lhs": lambda r1, r2, c1: r2/(r1+r2), "rhs": 0.6},
    {"lhs": lambda r1, r2, c1: (r1+r2)/(r1*r2*c1), "rhs": 2*pi*4000},
]


def load_db(comp_type, max_parts):
    fname = f"my_{'resistor' if comp_type=='R' else 'capacitor'}_db_{max_parts}combos.json"
    with open(f"combinations/{fname}", "r") as f:
        vals: dict = json.load(f)

    return {int(key): val for key, val in vals.items()}


all_r_combos = load_db("R", 3)
all_c_combos = load_db("C", 3)

r_vals = load_db(comp_type = "R", max_parts = 2).keys()
c_vals = load_db(comp_type = "C", max_parts = 2).keys()

def main():
    min_err_square = 999999999
    start_time_s = time()

    # Build the individual parts sets for each configured component
    sets = (load_db(c["type"], c["max_parts"]).keys() for c in components)

    for combination in product(*sets):

        # Turn capacitances involved from Picofarads into Farads for doing math with
        # This code sucks so much. Actual vomit. Please improve later.
        math_values = []
        for i, c in enumerate(components):
            if c["type"] == "C":
                math_values.append(combination[i] * 1e-12)
            else:
                math_values.append(combination[i])

        percent_errors = []
        err_square = 0

        for eq in equations:
            percent_err_n = eq["lhs"] (*math_values) - eq["rhs"]
            err_percent = 100 * (percent_err_n / eq["rhs"])

            percent_errors.append(err_percent)
            err_square += err_percent**2

        # Check if we found a new best solution
        if err_square < min_err_square:
            min_err_square = err_square

            elapsed_s_fmt = strftime('%H:%M:%S', gmtime(time() - start_time_s))

            print("-" * 50)

            # Print the formatted current percent errors
            print(f"error 1: {percent_errors[0]:<8.4f}%", end="")
            for n, percent_err_n in enumerate(percent_errors[1:], 1):
                print(f" | error {n+1:d}: {percent_err_n:<8.4f}%", end="")
            print()

            # Print the assembly instructions of each component involved
            for index, component_value in enumerate(combination):
                data = components[index]
                label = data["label"]
                formatted = format_resistor(component_value) if data["type"] == "R" else format_capacitor(component_value)
                assembly = all_r_combos[component_value] if data["type"] == "R" else all_c_combos[component_value]

                print(f"{label} = {formatted}: {assembly}")
            
            print(f"Elapsed time: {elapsed_s_fmt}")

print()
print("Optimal solution found.")

if __name__ == "__main__":
    main()