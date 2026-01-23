# Some AI-generated functions for taking care of component formatting

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


def to_picos(value):
    return int(round(value * 1e12))


def format_capacitor(value):
    """
    Format a capacitor value (given in farads) into schematic notation as strings.
    Converts to integer picofarads first and then formats as:
    - '100p' for picofarads
    - '1n', '4n7' for nanofarads
    - '10u', '2u2' for microfarads
    Handles up to about 1 millifarad.
    """
    # Convert to integer picofarads (pF)
    pf = to_picos(value)

    if pf < 1000:
        # <1000 pF: just show pF
        return f"{pf}p"
    elif pf < 1_000_000:
        # 1nF to 999nF
        nf = pf // 1000
        rem = pf % 1000
        if rem == 0:
            # Exact value
            return f"{nf}n"
        # Show remainder as one or two digits (e.g. 4n7 for 4700pF = 4.7nF)
        if rem % 100 == 0:
            return f"{nf}n{rem // 100}"
        elif rem % 10 == 0:
            return f"{nf}n{rem // 10:02}"
        else:
            return f"{nf}n{rem:03}"
    elif pf < 1_000_000_000:
        # 1uF to 999uF
        uf = pf // 1_000_000
        rem = pf % 1_000_000
        if rem == 0:
            return f"{uf}u"
        nf_rem = rem // 1000
        if nf_rem % 100 == 0:
            return f"{uf}u{nf_rem // 100}"
        elif nf_rem % 10 == 0:
            return f"{uf}u{nf_rem // 10:02}"
        else:
            return f"{uf}u{nf_rem:03}"
    else:
        # 1 millifarad or more (very rare)
        mf = pf / 1_000_000_000
        return f"{mf}m"