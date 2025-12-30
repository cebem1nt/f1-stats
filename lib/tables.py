def to_str(item: any, show_nones=False):
    if item is None:
        if show_nones:
            return "None"
        else:
            return " "

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
    show_nones=False,
    is_reversed=False,
    hide_delimiters=False
):
    header_line = ""
    med_separator = ""
    
    sep = '|' if not hide_delimiters else ' '
    hyph = '-' if not hide_delimiters else ' '

    for i, header in enumerate(headers):
        adjusted = adjust(to_str(header, show_nones), widths[i], adjustment)
        header_line += f"{sep} {adjusted} "
        med_separator += f"{sep}{hyph}{hyph * widths[i]}{hyph}"
    
    if is_reversed:
        print(med_separator + sep)
        print(header_line + sep)
    else:
        print(header_line + sep)
        print(med_separator + sep)

def print_rows(
    rows: list[any],
    widths: list[int],
    adjustment: str,
    show_nones=False,
    hide_delimiters=False
):
    line = ""
    sep = '|' if not hide_delimiters else ' '

    for row in rows:
        for i in range(len(row)):
            element = to_str(row[i], show_nones)
            line += f"{sep} {adjust(element, widths[i], adjustment)} "

        print(line + sep)
        line = ""

def print_table(
    rows: list[any],
    headers: list[str],
    adjustment="left",
    hide_delimiters=False,
    double_headers=False,
    show_nones=False
):
    if len(rows) and len(headers) != len(rows[0]):
        return

    widths = [len(to_str(h, show_nones)) for h in headers]

    for row in rows:
        for j in range(len(headers)):
            column_len = len(to_str(row[j]))
            
            if widths[j] < column_len:
                widths[j] = column_len

    print()
    print_headers(headers, widths, adjustment, show_nones, hide_delimiters=hide_delimiters)
    print_rows(rows, widths, adjustment, show_nones, hide_delimiters)
    
    if double_headers:
        print_headers(headers, widths, adjustment, show_nones, True, hide_delimiters)
    
    print()