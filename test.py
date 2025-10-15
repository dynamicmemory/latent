import csv 

fname: str = "example.csv"
data = [
    ["A", "B", "C"],
    ["D", "E", "F"],
    ["H", "I", "J"]
    ]

with open(fname, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(data[0])
    writer.writerows(data[1:])

print(f"Data written to {fname}") 

