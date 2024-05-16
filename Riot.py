import requests
import json


class Riot:
    def __init__(self, game_name, tag_line, prv, rrv):
        self.game_name = game_name
        self.tag_line = tag_line
        self.prv = prv  # platform routing value
        self.rrv = rrv  # regional routing value

        file = open("config.json")
        config = json.load(file)
        self.rgapi = config["RGAPI"]

        account_v1 = json.loads(requests.get(("https://{0}.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
                                              "/{1}/{2}?api_key=" + self.rgapi).format(self.rrv, self.game_name,
                                                                                       self.tag_line)).text)
        self.puuid = account_v1['puuid']

        summoner_v4 = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{"
                                               "1}?api_key=" + self.rgapi).format(self.prv, self.puuid)).text)
        self.summoner_id = summoner_v4["id"]  # also referred to as 'id' & 'encryptedSummonerId'
        self.account_id = summoner_v4["accountId"]
        self.profile_icon = "https://ddragon-webp.lolmath.net/latest/img/profileicon/{0}.webp".format(
            summoner_v4["profileIconId"])
        self.summoner_level = summoner_v4["summonerLevel"]

        