import requests
import json


class Teamfight:
    def __init__(self, account):
        self.account = account

    def ranked(self):
        league_v1 = json.loads(requests.get(("https://{0}.api.riotgames.com/tft/league/v1/entries/by-summoner/{"
                                            "1}?api_key=" + self.account.rgapi).format(self.account.prv,
                                                                                       self.account.summoner_id)).text)
        if len(league_v1) == 0:
            return "No ranked data present for this user."
        return league_v1

    def matches(self, count):
        match_v1 = json.loads(requests.get(("https://{0}.api.riotgames.com/tft/match/v1/matches/by-puuid/{"
                                            "1}/ids?start=0&count={2}&api_key=" + self.account.rgapi).format(
            self.account.rrv,
            self.account.puuid,
            count)).text)

        user_data = list()
        for i in range(len(match_v1)):
            match_data = json.loads(requests.get(("https://{0}.api.riotgames.com/tft/match/v1/matches/{1}?api_key=" +
                                                  self.account.rgapi).format(self.account.rrv, match_v1[i])).text)
            info = match_data["info"]
            participants = info["participants"]
            for j in range(len(participants)):
                if participants[j]['puuid'] == self.account.puuid:
                    missions = participants[j]["missions"]
                    info_set = {
                        "augments": participants[j]["augments"],
                        "players_eliminated": participants[j]["players_eliminated"],
                        "gold_left": participants[j]["gold_left"],
                        "last_round": participants[j]["last_round"],
                        "placement": participants[j]["placement"],
                        "time_eliminated": participants[j]["time_eliminated"],
                        "puuid": participants[j]["puuid"],
                        "traits": participants[j]["traits"],
                        "units": participants[j]["units"],
                        "gameCreation": info["gameCreation"],
                        "game_length": info["game_length"]
                    }
                    user_data.append(info_set)
        return user_data

