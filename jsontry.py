import json
# import urllib
# from urllib.request import urlopen

# resource = urllib.request.urlopen(an_url)
# content =  resource.read().decode(resource.headers.get_content_charset())

# violin =str(urlopen("https://www.googleapis.com/customsearch/v1?cx=018255618520952350685:8uiwqx6yz7m&key=AIzaSyDchAHDPniQvbs3FxRbr_dZyTbZQqmHs_M&q=Modi"))

# arr = json.loads(violin)

# print(violin)

import requests

link = "https://www.googleapis.com/customsearch/v1?cx=018255618520952350685:8uiwqx6yz7m&key=AIzaSyDchAHDPniQvbs3FxRbr_dZyTbZQqmHs_M&q=Modi"
f = requests.get(link)
arr = json.loads(f.text)
arr = arr['items']

for item in arr:
    print (item['title'],":",item['link'])