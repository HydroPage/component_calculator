from itertools import combinations
import json
from component_formatting import format_resistor

R_KIT = {10: 4, 22: 4, 47: 4, 100: 4, 220: 4, 470: 4, 1000: 8, 1200: 4, 1500: 4, 1800: 4, 
          2200: 4, 2700: 4, 3300: 4, 4700: 4, 5600: 4, 6800: 4, 8200: 4, 10000: 8, 15000: 4, 
          22000: 4, 33000: 4, 47000: 4, 56000: 4, 68000: 4, 82000: 4, 100000: 4}

"""
ECEN 325 kit
{10: 4, 22: 4, 47: 4, 100: 4, 220: 4, 470: 4, 1000: 8, 1200: 4, 1500: 4, 1800: 4, 
          2200: 4, 2700: 4, 3300: 4, 4700: 4, 5600: 4, 6800: 4, 8200: 4, 10000: 8, 15000: 4, 
          22000: 4, 33000: 4, 47000: 4, 56000: 4, 68000: 4, 82000: 4, 100000: 4}
"""

"""
ECEN 214 kit
{10: 2, 47: 2, 100: 2, 1000: 3, 2000: 2, 2200: 1, 3300: 1, 5100: 2, 10000: 2, 100000: 2, 360000: 1, 470000: 1}
"""

"""
My personal toolbox kit
{18: 10, 21: 10, 33: 10, 82: 10, 270: 10, 470: 10, 1500: 10, 2700: 10, 3900: 10, 
         6800: 10, 8200: 10, 18000: 10, 22000: 10, 33000: 10, 39000: 10, 47000: 10, 56000: 10, 
         68000: 10, 82000: 10, 150000: 10, 180000: 10, 390000: 10, 680000: 10, 820000: 10}
"""

r_vals = []
for (val, amt) in R_KIT.items():
    r_vals.extend([val] * amt)

r_2combos = set(combinations(r_vals, 2))
r_3combos = set(combinations(r_vals, 3))


def parallel(*resistors):
    inv_total = sum(1.0/r for r in resistors)
    return 1.0 / inv_total


def set_if_absent(dict, key, val):
    if key not in dict:
        dict[key] = val


num_combos = len(list(r_3combos))
num_computed = 0

all_values = {}

for r in r_vals:
    set_if_absent(all_values, round(r), f"{format_resistor(r)}")

all_values_sorted = {round(key): all_values[key] for key in sorted(all_values)}

with open("combinations/my_resistor_db_1combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)


for r1, r2 in r_2combos:
    r1_str = format_resistor(r1)
    r2_str = format_resistor(r2)

    set_if_absent(all_values, round(r1 + r2), f"{r1_str} + {r2_str}")
    set_if_absent(all_values, round(parallel(r1, r2)), f"{r1_str} || {r2_str}")

all_values_sorted = {round(key): all_values[key] for key in sorted(all_values)}

with open("combinations/my_resistor_db_2combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)


for r1, r2, r3 in r_3combos:
    r1_str = format_resistor(r1)
    r2_str = format_resistor(r2)
    r3_str = format_resistor(r3)

    # All series
    set_if_absent(all_values, round(r1 + r2 + r3), f"{r1_str} + {r2_str} + {r3_str}")

    # One series two parallel
    set_if_absent(all_values, round(r1 + parallel(r2, r3)), f"{r1_str} + ({r2_str} || {r3_str})")
    set_if_absent(all_values, round(r2 + parallel(r1, r3)), f"{r2_str} + ({r1_str} || {r3_str})")
    set_if_absent(all_values, round(r3 + parallel(r1, r2)), f"{r3_str} + ({r1_str} || {r2_str})")

    # One parallel two series
    set_if_absent(all_values, round(parallel(r1, r2 + r3)), f"{r1_str} || ({r2_str} + {r3_str})")
    set_if_absent(all_values, round(parallel(r2, r1 + r3)), f"{r2_str} || ({r1_str} + {r3_str})")
    set_if_absent(all_values, round(parallel(r3, r1 + r2)), f"{r3_str} || ({r1_str} + {r2_str})")

    # All parallel
    set_if_absent(all_values, round(parallel(r1, r2, r3)), f"{r1_str} || {r2_str} || {r3_str}")

    num_computed += 1
    print(f"{100*num_computed/num_combos:.2f}% complete")

all_values_sorted = {round(key): all_values[key] for key in sorted(all_values)}

with open("combinations/my_resistor_db_3combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)