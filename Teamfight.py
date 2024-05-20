import requests
import json


class Teamfight:
    def __init__(self, account):
        self.account = account

    def ranked(self, choice):
        summoner = json.loads(requests.get(("https://{0}.api.riotgames.com/tft/league/v1/entries/by-summoner/{"
                                            "1}?api_key=" + self.account.rgapi).format(self.account.prv,
                                                                                       self.account.summoner_id)).text)
        choice_queue = ""
        if choice == "double" or "double up" or "doubleup":
            choice_queue = "RANKED_TFT_DOUBLE_UP"
        if choice == "":
            choice_queue = "RANKED_TFT"

        for i in range(len(summoner)):
            if summoner[i].get('queueType') == choice_queue:
                return summoner[i]
        return "SuCo could not find the queue data for this summoner. Please try again with a different queue."

    def matches(self, count):
        match_v1 = json.loads(requests.get(("https://{0}.api.riotgames.com/tft/match/v1/matches/by-puuid/{"
                                            "1}/ids?start=0&count={2}&api_key=" + self.account.rgapi).format(
            self.account.rrv,
            self.account.puuid,
            count)).text)

        # Need to keep track of traits, total damage to players, kda, units and items, gold left, last round + time eliminated
        # https://developer.riotgames.com/docs/lol#data-dragon_data-assets
        for i in range(len(match_v1)):
            match_data = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/{1}?api_key=" +
                                                  self.account.rgapi).format(self.account.rrv, match_v1[i])).text)
            info = match_data["info"]
            info = info["participants"]
            players = list()
            for player in info:
                missions = player["missions"]
                info_set = {
                    "placement": player["placement"],
                    "players_eliminated": player["players_eliminated"],
                    "time_eliminated": player["time_eliminated"],
                    "gameCreation": player["gameCreation"],
                    "gold_left": player["gold_left"],
                    "last_round": player["last_round"],
                    "augments": player["augments"],
                    "kills": missions["kills"],
                    "deaths": missions["deaths"],
                    "assists": missions["assists"],
                    "TotalDamageDealtToChampions": player["TotalDamageDealtToChampions"],
                    "": player[""],

                }

        return match_v1
