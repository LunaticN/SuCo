import json

import requests

from LeagueRiot import League

# working with case --> ColdInfeno#0001 WorthlessRock #NA1

player = League("WorthlessRock", "NA1", "na1", "americas")
champs = player.champion_mastery("235")
print(champs)


champions = json.loads(requests.get("https://ddragon.leagueoflegends.com/cdn/14.8.1/data/en_US/champion.json").text)

print(type(champions))
