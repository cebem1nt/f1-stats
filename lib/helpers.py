from typing import Any

SUP_F = "\u1DA0"
SUP_P = "\u1D56"

def strsign(value: int):
    sign = '+' if value > 0 else ''
    return f"{sign}{value}"

def ifnone(data: Any, then: Any):
    return data if data is not None else then

def addif(data: Any, condition: bool, then: Any):
    return data + then if condition else data

def annotate_pf(data: Any, is_pole: bool, is_fastest: bool):
    return addif(
        addif(data, is_pole, SUP_P)
    , is_fastest, SUP_F)
    