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

    # Need to implement match data retrieval

