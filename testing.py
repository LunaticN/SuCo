from League import League
from Riot import Riot

account = Riot("ColdInfeno", "0001", "na1", "americas")
summoner = League(account)


print(summoner.matches(5))

# from Teamfight import Teamfight
#
# player = Teamfight("XcrazyAXL", "0224", "na1", "americas")
# print(player.puuid)
