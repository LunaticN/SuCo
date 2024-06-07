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

    def ranked(self):  # retrieves rank regardless of choice???
        league_v4 = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/league/v4/entries/by-summoner/{"
                                            "1}?api_key=" + self.account.rgapi).format(self.account.prv,
                                                                                       self.account.summoner_id)).text)
        if len(league_v4) == 0:
            return "No ranked data present for this user."
        return league_v4

    def matches(self, count):
        match_v5 = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/by-puuid/{"
                                            "1}/ids?start=0&count={2}&api_key=" + self.account.rgapi).format(
            self.account.rrv,
            self.account.puuid,
            count)).text)

        if len(match_v5) == 0:
            return "Unable to find requested match data for summoner" + self.account.game_name + "#" + \
                self.account.tag_line

        user_matches = list()
        for i in range(len(match_v5)):
            match_data = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/match/v5/matches/{1}?api_key=" +
                                                  self.account.rgapi).format(self.account.rrv, match_v5[i])).text)
            if 'status' in match_data:
                return "Data for match " + match_v5[i] + "could not be found as the match you are searching for may " \
                                                         "have expired beyond two years."
            info = match_data["info"]
            participants = info["participants"]
            for j in range(len(participants)):
                if participants[j]['puuid'] == self.account.puuid:
                    info_set = {"kills": participants[j]["kills"], "assists": participants[j]["assists"],
                                "deaths": participants[j]["deaths"], "champLevel": participants[j]["champLevel"],
                                "championId": participants[j]["championId"], "championName": participants[j]["championName"],
                                "championImg": "https://ddragon.leagueoflegends.com/cdn/14.8.1/img/champion/{0}.png"
                                .format(participants[j]["championName"]), "riotIdGameName": participants[j]["riotIdGameName"],
                                "riotIdTagline": participants[j]["riotIdTagline"],
                                "teamPosition": participants[j]["teamPosition"], "goldEarned": participants[j]["goldEarned"],
                                "wardsPlaced": participants[j]["wardsPlaced"], "wardsKilled": participants[j]["wardsKilled"],
                                "win": participants[j]["win"], "puuid": participants[j]["puuid"],
                                "totalDamageDealtToChampions": participants[j]["totalDamageDealtToChampions"],
                                "physicalDamageDealtToChampions": participants[j]["physicalDamageDealtToChampions"],
                                "magicDamageDealtToChampions": participants[j]["magicDamageDealtToChampions"],
                                "trueDamageDealtToChampions": participants[j]["trueDamageDealtToChampions"],
                                "doubleKills": participants[j]["doubleKills"], "tripleKills": participants[j]["tripleKills"],
                                "quadraKills": participants[j]["quadraKills"], "pentaKills": participants[j]["pentaKills"],
                                "summonerLevel": participants[j]["summonerLevel"],
                                "baronKills": participants[j]["baronKills"],
                                "magicDamageTaken": participants[j]["magicDamageTaken"],
                                "physicalDamageTaken": participants[j]["physicalDamageTaken"],
                                "trueDamageTaken": participants[j]["trueDamageTaken"],
                                "totalDamageTaken": participants[j]["totalDamageTaken"],
                                "gameCreation": info["gameCreation"],
                                "gameMode": info["gameMode"],
                                "mapId": info["mapId"]}
                    user_matches.append(info_set)
                    break
        return user_matches
