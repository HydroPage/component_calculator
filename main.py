from math import pi
import json


r_vals = {}
with open("combinations/my_resistor_db.json", "r") as f:
    r_vals = json.load(f)
    r_vals = {int(key): val for key, val in r_vals.items()}


c_vals = {}
with open("combinations/my_capacitor_db_3combos.json", "r") as f:
    c_vals = json.load(f)

    # Convert all from picofarads to float farads to do math with
    c_vals = {float(int(key) * 1e-12): val for key, val in c_vals.items()}


def main():
    print("Here we go")


if __name__ == "__main__":
    main()
