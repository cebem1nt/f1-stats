def to_str(item: any, empty_nones=False):
    if item is None:
        if empty_nones:
            return " "
        else:
            return "None"

    return str(item)

def adjust(
    item: str, 
    width: int,
    direction="left", 
):
    if direction == "left":
        return item.ljust(width)

    elif direction == "right":
        return item.rjust(width)

    else:
        return item.center(width)

def print_headers(
    headers: list[str],
    widths: list[int],
    adjustment: str,
    hide_nones=False,
    is_reversed=False
):
    header_line = ""
    med_separator = ""

    for i, header in enumerate(headers):
        width = widths[i]
        header_line += f"| {adjust(to_str(header, hide_nones), width, adjustment)} "
        med_separator   += f"|-{'-' * width}-"
    
    if is_reversed:
        print(med_separator + '|')
        print(header_line + '|')
        print()
    else:
        print()
        print(header_line + '|')
        print(med_separator + '|')

def print_rows(
    rows: list[any],
    widths: list[int],
    adjustment: str,
    hide_nones: bool
):
    line = ""

    for row in rows:
        for i in range(len(row)):
            element = to_str(row[i], hide_nones)
            line += f"| {adjust(element, widths[i], adjustment)} "

        print(line + '|')
        line = ""

def print_table(
    rows: list[any],
    headers: list[str],
    adjustment="left",
    hide_nones=False,
    double_headers=False
):
    if len(rows) and len(headers) != len(rows[0]):
        return

    widths = [len(to_str(h, hide_nones)) for h in headers]

    for row in rows:
        for j in range(len(headers)):
            column_len = len(to_str(row[j]))
            
            if widths[j] < column_len:
                widths[j] = column_len

    print_headers(headers, widths, adjustment, hide_nones)
    print_rows(rows, widths, adjustment, hide_nones)
    
    if double_headers:
        print_headers(headers, widths, adjustment, hide_nones, double_headers)