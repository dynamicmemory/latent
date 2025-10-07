def add_nums(num_list: list) -> int:
    total: int = 0
    for line in num_list:
        try:
            line.strip()
            line: int = int(line) 

            total += line 
        except:
            print("Line was not an int")
    return total


def read_lines(fname: str) -> list: 
    with open(fname, "r") as file:
        lines: list = file.readlines()

    file.close()
    return lines 


def write_line(line: str) -> None:
    with open(fname, "a") as file:
        file.write(line)
        file.close()
    

fname = "test.txt"
lines = read_lines(fname)
total = add_nums(lines)
write_line(str(total))
print([line.strip() for line in read_lines(fname)])
