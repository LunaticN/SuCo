import json
import requests
from LeagueRiot import League

summoner = League("ColdInfeno", "0001", "na1", "americas")

print(summoner.matches(5))
