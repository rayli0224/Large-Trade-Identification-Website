import json 

# Open the two JSON files
with open('file1.json') as f1, open('file2.json') as f2:
    # Load the JSON data from each file
    data1 = json.load(f1) 
    data2 = json.load(f2)  

# Compare the two JSON objects and store the differences in a list
differences = [] 
for key in data1:
    if key not in data2:
        differences.append({'key': key, 'status': 'missing', 'file': 'file2'})
    elif data1[key] != data2[key]:
        differences.append({'key': key, 'status': 'differs', 'value1': data1[key], 'value2': data2[key], 'file1': 'file1', 'file2': 'file2'})
for key in data2:
    if key not in data1: 
        differences.append({'key': key, 'status': 'missing', 'file': 'file1'})

# Print the list of differences in a formatted way
for diff in differences:
    if diff['status'] == 'missing': 
        print(f'{diff["key"]} is missing in {diff["file"]}')
    elif diff['status'] == 'differs':
        print(f'{diff["key"]} differs: {diff["value1"]} != {diff["value2"]} (in {diff["file1"]} vs {diff["file2"]})')