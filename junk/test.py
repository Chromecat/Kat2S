import json

with open('data.config') as json_file:
    data = json.load(json_file)
    print(data)
    test = int(data["density"])
    print(test)

