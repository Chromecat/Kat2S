import json

x = {
    "lat": "50.920652",
    "lon": "6.937008",
    "endtime": "10"
}

with open('data.config', 'w') as outfile:
    json.dump(x, outfile)
