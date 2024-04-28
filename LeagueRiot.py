import requests
import json


class League:
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

    def champion_mastery(self, champion_id):
        champion = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries"
                                            "/by-puuid/{1}/by-champion/{2}?api_key=" + self.rgapi).format(
            self.prv, self.puuid, champion_id)).text)
        return champion

    def ranked(self, choice):  # retrieves rank regardless of choice???
        summoner = json.loads(requests.get(
            ("https://{0}.api.riotgames.com/lol/league/v4/entries/by-summoner/{1}?api_key=" + self.rgapi).format(
                self.prv, self.summoner_id)).text)
        choice_queue = ""
        if choice == "solo" or "duo" or "solo/duo":
            choice_queue = "RANKED_SOLO_5x5"
        if choice == "flex":
            choice_queue = "RANKED_FLEX_SR"

        for i in range(len(summoner)):
            if summoner[i].get('queueType') == choice_queue:
                return summoner[i]
        return "SuCo could not find the queue data for this summoner. Please try again with a different queue."

    def matches(self, count):
        match_v5 = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/by-puuid/{"
                                            "1}/ids?start=0&count={2}&api_key=" + self.rgapi).format(self.rrv,
                                                                                                     self.puuid,
                                                                                                     count)).text)
        match_info_kahuna = list()
        for i in range(len(match_v5)):
            match_data = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/{1}?api_key=" +
                                                  self.rgapi).format(self.rrv, match_v5[i])).text)
            info = match_data["info"]
            info = info["participants"]
            players = list()
            for player in info:
                challenges = player["challenges"]
                info_set = {
                    "kills": player["kills"],
                    "assists": player["assists"],
                    "deaths": player["deaths"],
                    "kda": challenges["kda"],
                    "champLevel": player["champLevel"],  # champion related info
                    "championId": player["championId"],
                    "championName": player["championName"],
                    "championImg": "https://ddragon.leagueoflegends.com/cdn/14.8.1/img/champion/{0}.png"
                    .format(player["championName"]),
                    "teamPosition": player["teamPosition"],
                    "goldEarned": player["goldEarned"],
                    "wardsPlaced": player["wardsPlaced"],
                    "wardsKilled": player["wardsKilled"],
                    "win": player["win"],
                    "puuid": player["puuid"],
                    "totalDamageDealtToChampions": player["totalDamageDealtToChampions"],
                    "physicalDamageDealtToChampions": player["physicalDamageDealtToChampions"],
                    "magicDamageDealtToChampions": player["magicDamageDealtToChampions"],
                    "trueDamageDealtToChampions": player["trueDamageDealtToChampions"],
                    "doubleKills": player["doubleKills"],
                    "tripleKills": player["tripleKills"],
                    "quadraKills": player["quadraKills"],
                    "pentaKills": player["pentaKills"],
                    "summonerLevel": player["summonerLevel"],
                    "baronKills": player["baronKills"],
                    "magicDamageTaken": player["magicDamageTaken"],
                    "physicalDamageTaken": player["physicalDamageTaken"],
                    "trueDamageTaken": player["trueDamageTaken"],
                    "totalDamageTaken": player["totalDamageTaken"],
                    "maxCsAdvantageOnLaneOpponent": challenges["maxCsAdvantageOnLaneOpponent"],
                }
                players.append(info_set)
            match_info_kahuna.append(players)
            ginfo = match_data["info"]
            general_info = {
                "gameDuration": round(ginfo["gameDuration"] / 60),
                "gameCreation": ginfo["gameCreation"],
                "mapId": ginfo["mapId"],
                "endOfGameResult": ginfo["endOfGameResult"],
                "gameMode": ginfo["gameMode"],
                "gameType": ginfo["gameType"],
            }
            match_info_kahuna.append(general_info)
        return match_info_kahuna
