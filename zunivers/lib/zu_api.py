import requests
from datetime import datetime, timedelta
from .dtimestamp import DateTo

base_url = "https://zunivers-api.zerator.com/public/"
full_date_format = "%Y-%m-%dT%H:%M:%S"
discord_date_format = "%d/%m/%Y %H:%M"
vortex_date_format = "%Y-%m-%d"

def _get_player(url):
    with requests.get(url) as r:
        player_datas = r.json()

    return player_datas

def _get_challenge(url):
    with requests.get(url) as r:
        challenge_datas = r.json()

    return challenge_datas

class _User():

    def __init__(self, player_datas):
        user_json = player_datas["user"]

        self.name = user_json["discordUserName"]
        self.position = user_json["position"]
        self.score = user_json["score"]
        self.monnaie = user_json["balance"]
        self.poussiere = user_json["loreDust"]
        self.cristal = user_json["loreFragment"]
        self.rank = user_json["rank"]["name"]
        banner = user_json["userBanner"]["banner"]
        self.banner_name = banner["title"]
        self.banner_url = banner["imageUrl"]
        self.actif = user_json["isActive"]

class _ChallengeDatas():

    def __init__(self, datas):
        self.name = datas["challenge"]["description"]
        self.score = datas["challenge"]["score"]
        self.poussiere = datas["challenge"]["rewardLoreDust"]
        self.progress = f'{datas["progress"]["current"]}/{datas["progress"]["max"]}'
        achieved = datas["challengeLog"]
        if achieved == None:
            self.achieved_date = None
        else:
            self.achieved_date = DateTo(datetime.strptime(achieved["date"], full_date_format).strftime(discord_date_format)).longdate


class _Challenge():

    def __init__(self, challenge_datas):
        self.first = _ChallengeDatas(challenge_datas[0])
        self.second = _ChallengeDatas(challenge_datas[1])
        self.third = _ChallengeDatas(challenge_datas[2])
        # dates
        self.begin_date = DateTo(datetime.strptime(challenge_datas[0]["beginDate"], full_date_format).strftime(discord_date_format)).short_d
        self.end_date = DateTo(datetime.strptime(challenge_datas[0]["endDate"], full_date_format).strftime(discord_date_format)).short_d

class ZUniversProfile():

    def __init__(self, username, discri):
    # /jouer/username#discri datas
        self.player_url = f"{base_url}user/{username}%23{discri}"

        player_datas = _get_player(self.player_url)
        self.user = _User(player_datas)

        self.cards_nbrs = player_datas["inventoryCount"]
        # unique cards
        cards_nbrs_in_bdd = str(player_datas["itemCount"])
        self.unique_cards = f'{str(player_datas["inventoryUniqueCount"])}/{cards_nbrs_in_bdd}'
        self.unique_gold_cards = f'{str(player_datas["inventoryUniqueGoldenCount"])}/{cards_nbrs_in_bdd}'

        self.lr_nbrs = player_datas["luckyCount"]
        # achievments
        achievements_nbrs_in_bdd = str(player_datas["achievementCount"])
        self.achievements = f'{str(player_datas["achievementLogCount"])}/{achievements_nbrs_in_bdd}'
        # tradeless
        trades = player_datas["tradeCount"]
        if trades == 0:
            self.tradeless = ", Sans échange"
        else:
            self.tradeless = ""
        # subscription
        subscription = player_datas["subscription"]
        self.subscription_begin = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).longdate
        self.subscription_begin_since = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).relative
        self.subscription_end = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).short_d
        self.subscription_end_to = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).relative
        # pity
        days_before_pity = int(str(player_datas["invokeBeforePity"])[:-1])
        self.pity_in = DateTo((datetime.now() + timedelta(days=days_before_pity)).strftime(discord_date_format)).relative
        # vortex stats
        vortex_stats = player_datas["towerStat"]
        if vortex_stats["maxFloorIndex"] != None:
            self.vortex_stade = vortex_stats["maxFloorIndex"] + 1
        else:
            self.vortex_stade = 0
        self.vortex_trys = vortex_stats["towerLogCount"]
        self.vortex_begin_date = DateTo(datetime.strptime(vortex_stats["towerSeasonBeginDate"], vortex_date_format).strftime(discord_date_format)).short_d
        self.vortex_end_date = DateTo(datetime.strptime(vortex_stats["towerSeasonEndDate"], vortex_date_format).strftime(discord_date_format)).short_d
        self.vortex_name = vortex_stats["towerName"]
    # /challenge/username#discri datas
        challenge_url = f"{base_url}challenge/{username}%23{discri}"
        challenge_datas = _get_challenge(challenge_url)
        self.challenge = _Challenge(challenge_datas)


# a = ZUniversProfile("Aza'", "0428")
# print(a)