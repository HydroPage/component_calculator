from itertools import combinations
import json

R_KIT = {10: 4, 22: 4, 47: 4, 100: 4, 220: 4, 470: 4, 1000: 8, 1200: 4, 1500: 4, 1800: 4, 
          2200: 4, 2700: 4, 3300: 4, 4700: 4, 5600: 4, 6800: 4, 8200: 4, 10000: 8, 15000: 4, 
          22000: 4, 33000: 4, 47000: 4, 56000: 4, 68000: 4, 82000: 4, 100000: 4}

r_vals = []
for (val, amt) in R_KIT.items():
    r_vals.extend([val] * amt)

r_2combos = list(combinations(r_vals, 2))
r_3combos = list(combinations(r_vals, 3))




def parallel(*resistors):
    inv_total = sum(1.0/r for r in resistors)
    return 1.0 / inv_total


def format_resistor(value):
    """
    Format resistor value for schematics and part lists.
    Examples:
        470      -> '470'
        4700     -> '4k7'
        56000    -> '56k'
        680000   -> '680k'
        1000000  -> '1M'
        2200000  -> '2M2'
    """
    
    if value < 1000:
        return str(round(value))
    elif value < 1_000_000:
        kilo = value // 1000
        rem = value % 1000
        if rem == 0:
            return f"{kilo}k"
        # E.g.: 4700 -> 4k7, 47000 -> 47k, 5620 -> 5k62
        if rem % 100 == 0:
            return f"{kilo}k{rem // 100}"
        elif rem % 10 == 0:
            return f"{kilo}k{rem // 10:02}"
        else:
            return f"{kilo}k{rem:03}"
    else:
        mega = value // 1_000_000
        rem = value % 1_000_000
        if rem == 0:
            return f"{mega}M"
        
        # E.g.: 2_200_000 -> 2M2, 1_500_000 -> 1M5
        kilo_rem = rem // 1000
        if kilo_rem % 100 == 0:
            return f"{mega}M{kilo_rem // 100}"
        elif kilo_rem % 10 == 0:
            return f"{mega}M{kilo_rem // 10:02}"
        else:
            return f"{mega}M{kilo_rem:04}"


def set_if_absent(dict, key, val):
    if key not in dict:
        dict[key] = val


num_combos = len(list(r_3combos))
num_computed = 0

all_values = {}

for r in r_vals:
    set_if_absent(all_values, round(r), f"{format_resistor(r)}")

for r1, r2 in r_2combos:
    r1_str = format_resistor(r1)
    r2_str = format_resistor(r2)

    set_if_absent(all_values, round(r1 + r2), f"{r1_str} + {r2_str}")
    set_if_absent(all_values, round(parallel(r1, r2)), f"{r1_str} || {r2_str}")

all_values_sorted = {round(key): all_values[key] for key in sorted(all_values)}

with open("my_resistor_db_2combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)

for r1, r2, r3 in r_3combos:
    r1_str = format_resistor(r1)
    r2_str = format_resistor(r2)
    r3_str = format_resistor(r3)

    # All series
    set_if_absent(all_values, round(r1 + r2 + r3), f"{r1_str} + {r2_str} + {r3_str}")

    # One series two parallel
    set_if_absent(all_values, round(r1 + parallel(r1, r2)), f"{r1_str} + {r2_str} || {r3_str}")
    set_if_absent(all_values, round(r2 + parallel(r1, r3)), f"{r2_str} + {r1_str} || {r3_str}")
    set_if_absent(all_values, round(r3 + parallel(r2, r3)), f"{r3_str} + {r1_str} || {r2_str}")

    # One parallel two series
    set_if_absent(all_values, round(parallel(r1, r2 + r3)), f"{r1_str} || ({r2_str} + {r3_str})")
    set_if_absent(all_values, round(parallel(r2, r1 + r3)), f"{r2_str} || ({r1_str} + {r3_str})")
    set_if_absent(all_values, round(parallel(r3, r1 + r2)), f"{r3_str} || ({r1_str} + {r2_str})")

    # All parallel
    set_if_absent(all_values, round(parallel(r1, r2, r3)), f"{r1_str} || {r2_str} || {r3_str}")

    num_computed += 1
    print(f"{100*num_computed/num_combos:.2f}% complete")

all_values_sorted = {round(key): all_values[key] for key in sorted(all_values)}

with open("my_resistor_db_3combos.json", "w") as f:
    json.dump(all_values_sorted, f, indent=1)