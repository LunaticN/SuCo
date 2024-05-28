from League import League
from Riot import Riot

account = Riot("ColdInfeno", "0001", "na1", "americas")
account2 = Riot("Scruboyo", "她的亲爱的", "na1", "americas")
summoner = League(account)

print(account.puuid)
print(account2.account_id)

print(summoner.champion_mastery("Milio"))


