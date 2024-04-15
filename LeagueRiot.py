import os
import requests
import json

class League:
    def __init__(self, game_name, tag_line, region_code, region):
        self.game_name = game_name
        self.tag_line = tag_line
        self.region_code = region_code
        self.region = region  # make this a parameter that users put in using like a dropbox thing or something in an
        # embedded discord message..?

        with open('config.json') as file:
            config = json.loads(file)
            self.rgapi = config["RGAPI"]

        summoner_v4 = json.loads(requests.get(
            ("https://{0}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{1}?api_key=" + self.rgapi).format(
                self.region_code, self.game_name)).text)
        self.puuid = summoner_v4["puuid"]
        self.account_id = summoner_v4["accountId"]
        self.id = summoner_v4["id"]
        self.profile_icon = "https://ddragon-webp.lolmath.net/latest/img/profileicon/{0}.webp".format(
            summoner_v4["profileIconId"])
        # how many of these shits do i realistically need??^^
        # maybe add summonerLevel in constructor

    def champion_mastery(self, champion_id):
        champion = json.loads(requests.get(("https://{0}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries"
                                            "/by-puuid/{1}/by-champion/{2}?api_key=" + self.rgapi).format(
            self.region_code, self.puuid, champion_id)).text)
        # del champion["puuid"]
        # del champion["summonerId"]
        return champion

    def ranked(self, choice):  # retrieves rank regardless of choice???
        summoner = json.loads(requests.get(
            ("https://{0}.api.riotgames.com/lol/league/v4/entries/by-summoner/{1}?api_key=" + self.rgapi).format(
                self.region_code, self.id)).text)
        choice_queue = ""
        if choice == "solo" or "duo" or "solo/duo":
            choice_queue = "RANKED_SOLO_5x5"
        if choice == "flex":
            choice_queue = "RANKED_FLEX_SR"

        for i in range(len(summoner)):
            if summoner[i].get('queueType') == choice_queue:
                return summoner[i]
        return "SuCo could not find the queue data for this summoner. Please try again with a different queue."

# https://www.communitydragon.org/documentation/assets|
# inspo: https://imgur.com/a/PCvIY3w

# region_code = "na1" # BR1, EUN1, EUW1, LA1, LA2, NA1, OC1, RU1, TR1, JP1, KR, PH2, SG2, TW2, TH2, VN2
# print(champion_mastery[4]["championId"])
# rank = "DIAMOND"
# division = "III"

# ranked_search = json.loads(requests.get(("https://oc1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key=" + RGAPI)).text)
# print(ranked_search)
