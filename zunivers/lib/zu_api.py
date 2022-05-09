import requests
import discord
import urllib.parse
from datetime import datetime, timedelta
from .dtimestamp import DateTo

base_url = "https://zunivers-api.zerator.com/public/"
joueur_url = "https://zunivers.zerator.com/joueur/"
full_date_format = "%Y-%m-%dT%H:%M:%S"
discord_date_format = "%d/%m/%Y %H:%M"
vortex_date_format = "%Y-%m-%d"

def _get_datas(url):
    with requests.get(url) as r:
        datas = r.json()

    return datas

class Insomniaque():

    def __init__(self, user : discord.User):
        full_user = urllib.parse.quote(str(user))
        datas = _get_datas(f"{base_url}achievement/{full_user}/8e260bf0-f945-44b2-a9d9-92bf839ee917")
        insomniaque = datas[2]
        done = insomniaque["id"]

        self.name = insomniaque["achievement"]["name"]
        self.description = insomniaque["achievement"]["description"]
        self.reward_score = insomniaque["achievement"]["score"]
        if done:
            self.done = True
        else:
            self.done = False
            self.progress_done = []
            self.progress_todo = []

            for key, value in insomniaque["progress"]["items"].items():
                if value:
                    self.progress_done.append(key)
                else:
                    self.progress_todo.append(key)

class _ReputationClan():
    """attributs: name, level_name, progress"""

    def __init__(self, datas):
        score = datas["value"]
        level_max = datas["reputationLevel"]["toValue"] + 1

        self.name = datas["reputation"]["name"]
        self.level_name = datas["reputationLevel"]["name"]
        self.progress = f"{score}/{level_max}"

class _UserReputation():
    """attributs: first, second, third, fourth, fifth"""

    def __init__(self, datas):
        reputation_json = datas["reputations"]

        self.first = _ReputationClan(reputation_json[0])
        self.second = _ReputationClan(reputation_json[1])
        self.third = _ReputationClan(reputation_json[2])
        self.fourth = _ReputationClan(reputation_json[3])
        self.fifth = _ReputationClan(reputation_json[4])

class _ChallengeAtrb():
    """attributs: name, score_gain, powder_gain"""

    def __init__(self, datas):
        self.name = datas["challenge"]["description"]
        self.score_gain = datas["challenge"]["score"]
        self.powder_gain = datas["challenge"]["rewardLoreDust"]

class _UserChallengeAtrb():
    """attributs: name, score_gain, powder_gain, progress, achieved_date"""
    
    def __init__(self, datas):
        achieved = datas["challengeLog"]

        self.name = datas["challenge"]["description"]
        self.score_gain = datas["challenge"]["score"]
        self.powder_gain = datas["challenge"]["rewardLoreDust"]
        self.progress = f'{datas["progress"]["current"]}/{datas["progress"]["max"]}'
        if not achieved:
            self.achieved_date = None
        else:
            self.achieved_date = DateTo(datetime.strptime(achieved["date"], full_date_format).strftime(discord_date_format)).longdate

class Challenges():
    """attributs: first, second, third, begin_date, end_date"""

    def __init__(self, user : discord.User = None):
        full_user = urllib.parse.quote(str(user))
        datas = _get_datas(base_url + "challenge" + (f"/{full_user}" if user else ""))
        
        self.first = _ChallengeAtrb(datas[0])
        self.second = _ChallengeAtrb(datas[1])
        self.third = _ChallengeAtrb(datas[2])
        if user:
            self.first = _UserChallengeAtrb(datas[0])
            self.second = _UserChallengeAtrb(datas[1])
            self.third = _UserChallengeAtrb(datas[2])
        # dates
        self.begin_date = DateTo(datetime.strptime(datas[0]["beginDate"], full_date_format).strftime(discord_date_format)).short_d
        self.end_date = DateTo(datetime.strptime(datas[0]["endDate"], full_date_format).strftime(discord_date_format)).short_d

class Event:
    """attributs: got_events, names, pack_names, monney_costs, dust_costs, is_onetimes, begin_dates, end_dates, actives"""

    def __init__(self):
        datas = _get_datas(base_url + "event")

        if datas != []:
            self.got_events = True
            self.names = []
            self.pack_names = []
            self.monney_costs = []
            self.dust_costs = []
            self.is_onetimes = []
            self.begin_dates = []
            self.end_dates = []
            self.actives = []
            for i in range(len(datas)):
                self.names.append(datas[i]["name"])
                self.pack_names.append(datas[i]["pack"]["name"])
                self.monney_costs.append(datas[i]["balanceCost"])
                self.dust_costs.append(datas[i]["loreDustCost"])
                self.is_onetimes.append(datas[i]["isOneTime"])
                self.begin_dates.append(DateTo(datetime.strptime(datas[i]["beginDate"], full_date_format).strftime(discord_date_format)).longdate)
                self.end_dates.append(DateTo(datetime.strptime(datas[i]["endDate"], full_date_format).strftime(discord_date_format)).longdate)
                self.actives.append(datas[i]["isActive"])
        else:
            self.got_events = False

class Vortex:
    """attributs: name, pack, reputation, begin_date, end_date"""

    def __init__(self):
        datas_season = _get_datas(f"{base_url}tower/season")
        datas_stats = _get_datas(f"{base_url}tower/stats")

        self.name = datas_season["tower"]["name"]
        self.pack = datas_season["tower"]["pack"]["name"]
        self.reputation = datas_season["tower"]["reputation"]["name"]
        self.begin_date = DateTo(datetime.strptime(datas_season["beginDate"], vortex_date_format).strftime(discord_date_format)).short_d
        self.end_date = DateTo(datetime.strptime(datas_season["endDate"], vortex_date_format).strftime(discord_date_format)).short_d

class User():
    """arg: discord.User object"""

    def __init__(self, username : discord.User):
        full_user = urllib.parse.quote(str(username))
    ### datas ###
        user_datas = _get_datas(f"{base_url}user/{full_user}")
        challenge_datas = _get_datas(f"{base_url}challenge/{full_user}")
        reputation_datas = _get_datas(f"{base_url}tower/{full_user}")
        activity_datas = _get_datas(f"{base_url}user/{full_user}/activity")
    ### miscellaneous indexes ###
        user = user_datas["user"]
        total_card_numbers = str(user_datas["itemCount"])
        total_achievement_numbers = str(user_datas["achievementCount"])
        trades = user_datas["tradeCount"]
        subscription = user_datas["subscription"]
        days_before_pity = int(str(user_datas["invokeBeforePity"])[:-1])
        vortex_stats = user_datas["towerStat"]
        last_loot_count = activity_datas["lootInfos"][364]["count"]
    ### attributes ###
        self.url = f"{joueur_url}{full_user}"
        self.name = user["discordUserName"]
        self.position = user["position"]
        self.score = user["score"]
        self.monnaie = user["balance"]
        self.powder = user["loreDust"]
        self.crystal = user["loreFragment"]
        self.rank = user["rank"]["name"]
        self.active = user["isActive"]

        self.card_numbers = user_datas["inventoryCount"]
        self.unique_cards = f'{str(user_datas["inventoryUniqueCount"])}/{total_card_numbers}'
        self.unique_gold_cards = f'{str(user_datas["inventoryUniqueGoldenCount"])}/{total_card_numbers}'
        self.lucky_numbers = user_datas["luckyCount"]
        self.achievement_numbers = f'{str(user_datas["achievementLogCount"])}/{total_achievement_numbers}'
        if trades == 0:
            self.tradeless = True
        else:
            self.tradeless = False
        if subscription:
            self.is_subscribed = True
            self.subscription_begin = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).longdate
            self.subscription_begin_since = DateTo(datetime.strptime(subscription["beginDate"], full_date_format).strftime(discord_date_format)).relative
            self.subscription_end = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).short_d
            self.subscription_end_to = DateTo(datetime.strptime(subscription["endDate"], full_date_format).strftime(discord_date_format)).relative
        else:
            self.is_subscribed = False
        self.pity_in = DateTo((datetime.now() + timedelta(days=days_before_pity)).strftime(discord_date_format)).relative
        if vortex_stats:
            if vortex_stats["maxFloorIndex"]:
                self.vortex_stade = vortex_stats["maxFloorIndex"] + 1
            else:
                self.vortex_stade = 0
            self.vortex_trys = vortex_stats["towerLogCount"]
        else:
            self.vortex_stade = 0
            self.vortex_trys = 0
        ### sub-classes ###
        self.challenge = Challenges(username)
        self.reputation = _UserReputation(reputation_datas)
        if last_loot_count == 0:
            self.journa = False
        else:
            self.journa = True