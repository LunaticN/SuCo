import requests
import json


class Teamfight:
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
