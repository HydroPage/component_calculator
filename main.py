from math import pi
from time import time, strftime, gmtime
import json
from component_formatting import format_resistor, format_capacitor


r_vals = {}
with open("combinations/my_resistor_db_3combos.json", "r") as f:
    r_vals = json.load(f)
    r_vals = {int(key): val for key, val in r_vals.items()}


c_vals = {}
with open("combinations/my_capacitor_db_2combos.json", "r") as f:
    c_vals = json.load(f)

    # Convert all from picofarads to float farads to do math with
    c_vals = {float(int(key) * 1e-12): val for key, val in c_vals.items()}


def main():
    min_err_square = 999999999
    combo = {"C2": 0, "C3": 0, "R3": 0}

    start_time_s = time()

    for r3, r3_combo in r_vals.items():
        for c2, c2_combo in c_vals.items():
            for c3, c3_combo in c_vals.items():
                exp1_desired = 0.6
                exp2_desired = 2*pi*4000
                exp1 = c2 / (c2 + c3)
                exp2 = 1/(r3*(c2+c3))

                err1 = exp1 - exp1_desired
                err2 = exp2 - exp2_desired

                err1_percent = 100*(err1 / exp1_desired)
                err2_percent = 100*(err2 / exp2_desired)

                err_square = err1_percent**2 + err2_percent**2
                if err_square < min_err_square:
                    min_err_square = err_square
                    combo["C2"] = c2
                    combo["C3"] = c3
                    combo["R3"] = r3

                    elapsed_s_fmt = strftime('%H:%M:%S', gmtime(time() - start_time_s))

                    print("-" * 50)
                    print(f"err1: {err1_percent:<8.4f} % | err2: {err2_percent:<8.4f}%")
                    print(f"C2 = {format_capacitor(c2)}: {c2_combo}")
                    print(f"C3 = {format_capacitor(c3)}: {c3_combo}")
                    print(f"R3 = {format_resistor(r3)}: {r3_combo}")
                    print(f"Elapsed time: {elapsed_s_fmt}")


if __name__ == "__main__":
    main()