import requests
import json

url = "https://api.pubg.com/shards/steam/players/bbakker/seasons/division.bro.official.pc-2018-02"

url2= "https://api.pubg.com/shards/steam/seasons"

url3 = "https://api.pubg.com/shards/steam/players/BBAKKER"

apikey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMDkwZGM5MC0yODMzLTAxMzctMDE0ZC0zZDcxYmE4MjMzMWUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUyNTMyMzUwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImVvZGdrZWtkIn0.M9Lou5r1gJbd2ikEzl02dp6JbWnIy9ALDfqkcsugyGM"
header = {
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMDkwZGM5MC0yODMzLTAxMzctMDE0ZC0zZDcxYmE4MjMzMWUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUyNTMyMzUwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImVvZGdrZWtkIn0.M9Lou5r1gJbd2ikEzl02dp6JbWnIy9ALDfqkcsugyGM",
  "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)

json_data = r.json()

print(r)
print(r.text)

print(json_data)
