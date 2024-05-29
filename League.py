import requests
import json

#https://developer.riotgames.com/docs/lol#data-dragon_data-assets

class League:
    def __init__(self, account):
        self.account = account

    def champion_mastery(self, champion_name):
        try:
            champion_name = champion_name.lower()
            champion_name_first_letter = champion_name[0].upper()
            champion_name = champion_name_first_letter + champion_name[1:]
            champions_data = json.loads(requests.get("https://ddragon.leagueoflegends.com/cdn/14.10.1/data/en_US/champion"
                                                     ".json").text)
            champions_data = champions_data["data"]
            champions_data = champions_data[champion_name]
            champion_id = champions_data["key"]

            champion = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries"
                                                "/by-puuid/{1}/by-champion/{2}?api_key=" + self.account.rgapi).format(
                self.account.prv, self.account.puuid, champion_id)).text)
            if 'status' in champion:
                champion = "No data available for this champion."
        except:
            champion = "Unable to find champion :("
        return champion

    def ranked(self, choice):  # retrieves rank regardless of choice???
        summoner = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/league/v4/entries/by-summoner/{"
                                            "1}?api_key=" + self.account.rgapi).format(self.account.prv,
                                                                                       self.account.summoner_id)).text)
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
                                            "1}/ids?start=0&count={2}&api_key=" + self.account.rgapi).format(
            self.account.rrv,
            self.account.puuid,
            count)).text)
        match_info_kahuna = list()
        for i in range(len(match_v5)):
            match_data = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/{1}?api_key=" +
                                                  self.account.rgapi).format(self.account.rrv, match_v5[i])).text)
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
                    "riotIdGameName": player["riotIdGameName"],
                    "riotIdTagline": player["riotIdTagline"],
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
    # https://ddragon.leagueoflegends.com/cdn/14.10.1/img/item/1001.png

