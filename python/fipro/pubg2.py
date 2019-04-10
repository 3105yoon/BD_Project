from pubg_python import PUBG, Shard

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMDkwZGM5MC0yODMzLTAxMzctMDE0ZC0zZDcxYmE4MjMzMWUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTUyNTMyMzUwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImVvZGdrZWtkIn0.M9Lou5r1gJbd2ikEzl02dp6JbWnIy9ALDfqkcsugyGM"
api = PUBG(api_key, Shard.PC_KRJP)


sample = api.samples().get()
for match in sample.matches:
    print(match.id)


#player = api.players().get('account.d50fdc18fcad49c691d38466bed6f8fd')
#for match in player.matches:
#    match_data = api.matches.get(match.id)
    
