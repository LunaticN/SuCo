# from League import League
from Riot import Riot
#
account = Riot("GodProfits", "3541", "na1", "americas")
account2 = Riot("Coldinfeno", "0001", "na1", "americas")
# summoner = League(account)
#
#
# print(summoner.matches(5))

from Teamfight import Teamfight
summoner = Teamfight(account)

print(account.puuid)
print(summoner.matches(4))
