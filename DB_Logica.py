import json

with open('Config.json', 'r', encoding='utf-8') as read_file:
    data = json.load(read_file)
    dict1 = dict(data)

print(data)
key = list(dict1["Language"].keys())
print(data["Language"]["Russian"])
print(key)