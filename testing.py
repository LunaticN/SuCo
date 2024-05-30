from League import League
from Riot import Riot

account = Riot("ColdInfeno", "0001", "na1", "americas")
account2 = Riot("Scruboyo", "她的亲爱的", "na1", "americas")
account3 = Riot("Yozu", "Lux", "na1", "americas")
account4 = Riot("Ricoishot", "NA1", "na1", "americas")
summoner = League(account)
summoner3 = League(account3)
summoner4 = League(account4)

# print(account.puuid)
# print(account2.account_id)
# print(account3.summoner_id)
# print(account4.summoner_id)

print(summoner.champion_mastery("qiyana"))
print(summoner3.ranked())

