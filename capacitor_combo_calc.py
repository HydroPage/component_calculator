from itertools import combinations
import json
from component_formatting import format_capacitor, to_picos

C_KIT = {100e-12: 2, 1e-9: 2, 4.7e-9: 2, 10e-9: 2, 33e-9: 2, 
          47e-9: 2, 100e-9: 2, 220e-9: 2, 470e-9: 2, 10e-6: 4}

c_vals = []
for (val, amt) in C_KIT.items():
    c_vals.extend([val] * amt)

c_2combos = list(combinations(c_vals, 2))
c_3combos = list(combinations(c_vals, 3))


def series(*caps):
    inv_total = sum(1.0/c for c in caps)
    return 1.0 / inv_total


def set_if_absent(dict, key, val):
    if key not in dict:
        dict[key] = val


num_combos = len(c_vals) + len(list(c_2combos)) + len(list(c_3combos))
num_computed = 0

all_values = {}

for c in c_vals:
    set_if_absent(all_values, to_picos(c), f"{format_capacitor(c)}")

    num_computed += 1
    print(f"{100*num_computed/num_combos:.2f}% complete")

all_values_sorted = {key: all_values[key] for key in sorted(all_values)}

with open("combinations/my_capacitor_db_singles.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)


for c1, c2 in c_2combos:
    c1_str = format_capacitor(c1)
    c2_str = format_capacitor(c2)

    set_if_absent(all_values, to_picos(c1 + c2), f"{c1_str} + {c2_str}")
    set_if_absent(all_values, to_picos(series(c1, c2)), f"{c1_str} || {c2_str}")

    num_computed += 1
    print(f"{100*num_computed/num_combos:.2f}% complete")

all_values_sorted = {key: all_values[key] for key in sorted(all_values)}

with open("combinations/my_capacitor_db_2combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)


for c1, c2, c3 in c_3combos:
    c1_str = format_capacitor(c1)
    c2_str = format_capacitor(c2)
    c3_str = format_capacitor(c3)

    # All parallel
    set_if_absent(all_values, to_picos(c1 + c2 + c3), f"{c1_str} || {c2_str} || {c3_str}")

    # One parallel two series
    set_if_absent(all_values, to_picos(c1 + series(c1, c2)), f"{c1_str} || {c2_str} + {c3_str}")
    set_if_absent(all_values, to_picos(c2 + series(c1, c3)), f"{c2_str} || {c1_str} + {c3_str}")
    set_if_absent(all_values, to_picos(c3 + series(c2, c3)), f"{c3_str} || {c1_str} + {c2_str}")

    # One series two parallel
    set_if_absent(all_values, to_picos(series(c1, c2 + c3)), f"{c1_str} + ({c2_str} || {c3_str})")
    set_if_absent(all_values, to_picos(series(c2, c1 + c3)), f"{c2_str} + ({c1_str} || {c3_str})")
    set_if_absent(all_values, to_picos(series(c3, c1 + c2)), f"{c3_str} + ({c1_str} || {c2_str})")

    # All series
    set_if_absent(all_values, to_picos(series(c1, c2, c3)), f"{c1_str} + {c2_str} + {c3_str}")

    num_computed += 1
    print(f"{100*num_computed/num_combos:.2f}% complete")


all_values_sorted = {key: all_values[key] for key in sorted(all_values)}

with open("combinations/my_capacitor_db_3combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)