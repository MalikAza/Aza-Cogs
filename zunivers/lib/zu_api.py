import requests
from datetime import datetime, timedelta
from .dtimestamp import DateTo

base_url = "https://zunivers-api.zerator.com/public/"
joueur_url = "https://zunivers.zerator.com/joueur/"
full_date_format = "%Y-%m-%dT%H:%M:%S"
discord_date_format = "%d/%m/%Y %H:%M"
vortex_date_format = "%Y-%m-%d"

# TODO  - journa (et bonus ?) => https://zunivers-api.zerator.com/public/user/Aza'%230428/activity
#       - graphs stats => https://zunivers-api.zerator.com/public/user/Aza'%230428/userscorelog?duration=P7D

def _get_datas(url):
    with requests.get(url) as r:
        datas = r.json()

    return datas

class _User():

    def __init__(self, player_datas):
        user_json = player_datas["user"]
        banner = user_json["userBanner"]["banner"]

        self.name = user_json["discordUserName"]
        self.position = user_json["position"]
        self.score = user_json["score"]
        self.monnaie = user_json["balance"]
        self.poussiere = user_json["loreDust"]
        self.cristal = user_json["loreFragment"]
        self.rank = user_json["rank"]["name"]
        self.banner_name = banner["title"]
        self.banner_url = banner["imageUrl"]
        self.actif = user_json["isActive"]

class _ChallengeDatas():

    def __init__(self, datas):
        achieved = datas["challengeLog"]

        self.name = datas["challenge"]["description"]
        self.score = datas["challenge"]["score"]
        self.poussiere = datas["challenge"]["rewardLoreDust"]
        self.progress = f'{datas["progress"]["current"]}/{datas["progress"]["max"]}'
        if achieved == None:
            self.achieved_date = None
        else:
            self.achieved_date = DateTo(datetime.strptime(achieved["date"], full_date_format).strftime(discord_date_format)).longdate

class _Clan():

    def __init__(self, index):
        score = index["value"]
        level_max = index["reputationLevel"]["toValue"] + 1

        self.name = index["reputation"]["name"]
        self.level_name = index["reputationLevel"]["name"]
        self.progress = f"{score}/{level_max}"

class _Reputation():

    def __init__(self, datas):
        reputation_json = datas["reputations"]

        self.one = _Clan(reputation_json[0])
        self.two = _Clan(reputation_json[1])
        self.three = _Clan(reputation_json[2])
        self.four = _Clan(reputation_json[3])
        self.five = _Clan(reputation_json[4])

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
        full_user = f"{username}%23{discri}"
    ### urls, base datas ###
        # /user/
        player_url = f"{base_url}user/{full_user}"
        player_datas = _get_datas(player_url)
        # /challenge/
        challenge_url = f"{base_url}challenge/{full_user}"
        challenge_datas = _get_datas(challenge_url)
        # /tower/
        reputation_url = f"{base_url}tower/{full_user}"
        reputation_datas = _get_datas(reputation_url)
    ### miscellaneous indexes ###
        cards_nbrs_in_bdd = str(player_datas["itemCount"])
        achievements_nbrs_in_bdd = str(player_datas["achievementCount"])
        trades = player_datas["tradeCount"]
        subscription = player_datas["subscription"]
        days_before_pity = int(str(player_datas["invokeBeforePity"])[:-1])
        vortex_stats = player_datas["towerStat"]
        
        self.player_url = f"{joueur_url}{full_user}"
    ### sub-class ###
        self.user = _User(player_datas)
        self.challenge = _Challenge(challenge_datas)
        self.reputation = _Reputation(reputation_datas)
    ### general player_datas ###
        self.cards_nbrs = player_datas["inventoryCount"]
        # unique cards
        self.unique_cards = f'{str(player_datas["inventoryUniqueCount"])}/{cards_nbrs_in_bdd}'
        self.unique_gold_cards = f'{str(player_datas["inventoryUniqueGoldenCount"])}/{cards_nbrs_in_bdd}'
        # lucky rayou
        self.lr_nbrs = player_datas["luckyCount"]
        # achievments
        self.achievements = f'{str(player_datas["achievementLogCount"])}/{achievements_nbrs_in_bdd}'
        # tradeless
        if trades == 0:
            self.tradeless = ", Sans échange"
        else:
            self.tradeless = ""
        # subscription
        self.subscription_begin = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).longdate
        self.subscription_begin_since = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).relative
        self.subscription_end = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).short_d
        self.subscription_end_to = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).relative
        # pity
        self.pity_in = DateTo((datetime.now() + timedelta(days=days_before_pity)).strftime(discord_date_format)).relative
        # vortex stats
        if vortex_stats["maxFloorIndex"] != None:
            self.vortex_stade = vortex_stats["maxFloorIndex"] + 1
        else:
            self.vortex_stade = 0
        self.vortex_trys = vortex_stats["towerLogCount"]
        self.vortex_begin_date = DateTo(datetime.strptime(vortex_stats["towerSeasonBeginDate"], vortex_date_format).strftime(discord_date_format)).short_d
        self.vortex_end_date = DateTo(datetime.strptime(vortex_stats["towerSeasonEndDate"], vortex_date_format).strftime(discord_date_format)).short_d
        self.vortex_name = vortex_stats["towerName"]
