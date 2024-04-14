import json

import requests

dictionary = json.loads(requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/EoiXpjHDfsL9X606ou3MyuZ7XYBELAuJYSYFE4TtXXpN2WQ?api_key=RGAPI-c8866cb7-beb4-4a8e-8872-2d190eed09ae").text)


for i in range(len(dictionary)):
    if dictionary[i].get('queueType') == "RANKED_FLEX_SR":
        print(dictionary[i])
    print("SuCo could not find the queue data for this summoner. Please try again with a different queue.")

print(dictionary)
