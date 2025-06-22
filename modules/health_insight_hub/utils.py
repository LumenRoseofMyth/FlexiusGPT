def round_or_none(value, decimals=1):
    try:
        return round(float(value), decimals)
    except:
        return None
