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
        # del champion["puuid"]
        # del champion["summonerId"]
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

# https://www.communitydragon.org/documentation/assets|
# inspo: https://imgur.com/a/PCvIY3w

# region_code = "na1" # BR1, EUN1, EUW1, LA1, LA2, NA1, OC1, RU1, TR1, JP1, KR, PH2, SG2, TW2, TH2, VN2
# print(champion_mastery[4]["championId"])
# rank = "DIAMOND"
# division = "III"

# ranked_search = json.loads(requests.get(("https://oc1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key=" + RGAPI)).text)
# print(ranked_search)
