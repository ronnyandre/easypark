import easypark as ep
import json

ep.username = None
ep.password = None
ep.user_id = None

parkings = ep.list_parkings()

print(parkings)

with open('parkings.json', 'w') as f:
    json.dump(parkings, f)