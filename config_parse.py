# Import "*" because I want eval() to pick up on any conventional
# math functions from the JSON script like sqrt() or sin(), etc.
from math import *
import json


# Format the comma-separated arguments into a comma-separated string
def format_commas(*args):
    out = str(args[0])
    for i in range(len(args) - 1):
        out += ", " + str(args[i + 1])
    
    return out


# Parses an equation object, {"lhs": expression, "rhs": constant} using the variable names as inputs
# Returns a new dict with a multivariable function in "lhs" and a goal constant float in "rhs"
def parse_equation(eq_object: dict[str, str], *var_names: list[str]):
    comma_sep_var_names = format_commas(*var_names)

    # Demonic "eval(...)" code to turn the JSON strings into executable code:
    lhs_lambda = eval(f"lambda {comma_sep_var_names}: {eq_object['lhs']}")
    rhs_constant = float(eval(eq_object["rhs"]))

    return {"lhs": lhs_lambda, "rhs": rhs_constant}


# Open the configuration file, and transform it from JSON into executable code
def parse_config_file(file_name = "config.json"):
    with open(file_name, "r") as f:
        data = json.load(f)
        components = data["components"]

        part_labels = [c["label"] for c in components]
        equations = [parse_equation(eq, *part_labels) for eq in data["equations"]]
    
    return components, equations