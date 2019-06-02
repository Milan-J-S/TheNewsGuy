import json

f = open("some.json")
j = json.load(f)

arr = j['items']

for item in arr:
    print (item['title'],":",item['link'])