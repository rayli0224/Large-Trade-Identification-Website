import csv

def get_additional_info(file1, file2, output_file):
    data1 = []
    with open(file1, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data1.append(row)

    data2 = []
    with open(file2, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data2.append(row)

    additional_rows = [row for row in data2 if row not in data1]

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in additional_rows:
            writer.writerow(row)