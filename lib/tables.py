def to_str(item: any):
    return str(item) if item else "None"

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
    adjustment: str
):
    header_line = ""
    separator = ""

    for i, header in enumerate(headers):
        width = widths[i]
        header_line += f"| {adjust(header, width, adjustment)} "
        separator   += f"|-{'-' * width}-"
    
    print(header_line + '|')
    print(separator + '|')

def print_rows(
    rows: list[any],
    widths: list[int],
    adjustment: str
):
    line = ""

    for row in rows:
        for i in range(len(row)):
            element = to_str(row[i])
            line += f"| {adjust(element, widths[i], adjustment)} "

        print(line + '|')
        line = ""

def print_table(
    rows: list[any],
    headers: list[str],
    adjustment="left"
):
    if len(rows) and len(headers) != len(rows[0]):
        return

    widths = [len(h) for h in headers]

    for row in rows:
        for j in range(len(headers)):
            column_len = len(to_str(row[j]))
            
            if widths[j] < column_len:
                widths[j] = column_len

    print_headers(headers, widths, adjustment)
    print_rows(rows, widths, adjustment)