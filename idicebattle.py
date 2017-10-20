#cog.name inspired by Hitsumo
#Idea developped by Aza' & Hitsumo
#cog coding par Aza'
import discord
from discord.ext import commands
from random import randint
from cogs.utils.dataIO import dataIO
from copy import deepcopy
from __main__ import send_cmd_help
from cogs.utils import checks
import os
import logging
import asyncio

default_server_config = {}

class IDiceError(Exception):
    pass

class AlreadyRegistered(IDiceError):
    pass

class NotRegistered(IDiceError):
    pass

class NotConfigured(IDiceError):
    pass

class AlreadyConfigured(IDiceError):
    pass

class IDiceBattle:
    def __init__(self, bot):
        self.bot = bot
        self.profile_path = "data/iDice/profile.json"
        self.config_path = "data/iDice/config.json"
        self.profiles = dataIO.load_json(self.profile_path)
        self.config = dataIO.load_json(self.config_path)

    def create_profile(self, user, server):
        if not self.profile_exists(user, server):
            profile = {"lvl": 1,
                         "exp" : 0,
                         "bonus" : 0
                         }
            self.profiles["servers"][server.id][user.id] = profile
            self._save_profile()
        else:
            raise AlreadyRegistered()

    def profile_exists(self, user, server):
        try:
            self._get_profile(user, server)
        except NotRegistered:
            return False
        return True

    def config_exists(self, server):
        try:
            self._get_config(server)
        except NotConfigured:
            return False
        return True

    def enough_emojis(self, server):
        list_emoji = list(emoji.name for emoji in server.emojis)
        if len(list_emoji) <= 46:
            return True
        else:
            return False

    def add_server_config(self, server):
        if not self.config_exists(server):
            server_config = default_server_config
            self.config["servers"][server.id] = server_config
            self._save_config()
            self.profiles["servers"][server.id] = {}
            self._save_profile()
        else:
            raise AlreadyConfigured

    def get_lvl(self, user, server):
        profile = self._get_profile(user, server)
        return profile["lvl"]

    def get_exp(self, user, server):
        profile = self._get_profile(user, server)
        return profile["exp"]

    def exp_up(self, user, server):
        profile = self._get_profile(user, server)
        exp = profile["exp"]
        lvl = profile["lvl"]
        possible_futur_exp = (exp + 1)
        if possible_futur_exp > (10*lvl):
            self.lvl_up(user, server)
        else:
            profile["exp"] += 1
            self.profiles["servers"][server.id][user.id] = profile
            self._save_profile()

    def get_bonus(self, user, server):
        profile = self._get_profile(user, server)
        return profile["bonus"]

    def lvl_up(self, user):
        profile = self._get_profile(user, server)
        profile["lvl"] += 1
        profile["exp"] = 0
        profile["bonus"] += 1
        self.profiles["servers"][server.id][user.id] = profile
        self._save_profile()

    def _save_profile(self):
        dataIO.save_json("data/iDice/profile.json", self.profiles)

    def _save_config(self):
        dataIO.save_json("data/iDice/config.json", self.config)

    def _get_profile(self, user, server):
        try:
            return deepcopy(self.profiles["servers"][server.id][user.id])
        except KeyError:
            raise NotRegistered()

    def _get_config(self, server):
        try:
            return deepcopy(self.config["servers"][server.id])
        except KeyError:
            raise NotConfigured()

    def dice_author(self, author, server):
        crit_failure = discord.utils.get(server.emojis, name="crit_failure_dice")
        failure = discord.utils.get(server.emojis, name="failure_dice")
        normal = discord.utils.get(server.emojis, name="normal_dice")
        crit_success = discord.utils.get(server.emojis, name="crit_success_dice")
        n1_author = randint(1, 10)
        bonus_author = self.get_bonus(author, server)
        if n1_author == 10:#Critical success
            n2_author = randint(1, 10)
            n_author = n1_author + n2_author
            dice_author = crit_success
            bonus_author = bonus_author + int((0.50*bonus_author))
            if bonus_author != 0:
                n_author = n_author + bonus_author
        elif n1_author == 1:#Failure
            n2_author = randint(1, 10)
            n_author = n1_author + n2_author
            if n2_author == 1:#Critical failure
                dice_author =crit_failure
            else:#Failure (following)
                dice_author = failure
                bonus_author = bonus_author - int((0.25*bonus_author))
            if bonus_author != 0:
                n_author = n_author + bonus_author
                bonus_author = bonus_author - int((0.50*bonus_author))
        elif n1_author != 10 and n1_author != 1:#Normal
            dice_author = normal
            n_author = n1_author
            if bonus_author != 0:
                n_author = n_author + bonus_author
        dict_dice_author = {"dice_author" : dice_author, "n_author" : n_author}
        return dict_dice_author

    def dice_user(self, user, server):
        crit_failure = discord.utils.get(server.emojis, name="crit_failure_dice")
        failure = discord.utils.get(server.emojis, name="failure_dice")
        normal = discord.utils.get(server.emojis, name="normal_dice")
        crit_success = discord.utils.get(server.emojis, name="crit_success_dice")
        n1_user = randint(1, 10)
        bonus_user = self.get_bonus(user, server)
        if n1_user == 10:#Critical success
            n2_user = randint(1, 10)
            n_user = n1_user + n2_user
            dice_user = crit_success
            bonus_user = bonus_user + int((0.50*bonus_user))
            if bonus_user != 0:
                n_user = n_user + bonus_user
        elif n1_user == 1:#Failure
            n2_user = randint(1, 10)
            n_user = n1_user + n2_user
            if n2_user == 1:#Critical failure
                dice_user = crit_failure
            else:#Failure (following)
                dice_user = failure
                bonus_user = bonus_user - int((0.25*bonus_user))
            if bonus_user != 0:
                n_user = n_user + bonus_user
                bonus_user = bonus_user - int((0.50*bonus_user))
        elif n1_user != 10 and n1_user != 1:#Normal
            dice_user = normal
            n_user = n1_user
            if bonus_user != 0:
                n_user = n_user + bonus_user
        dict_dice_user = {"dice_user" : dice_user, "n_user" : n_user}
        return dict_dice_user

    def results(self, author, user, n_author, n_user, dice_author, dice_user, bank, amount):
        msg = ""
        winner = ""
        loser = ""
        server = author.server
        if n_author > n_user:
            #Winner
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            #Loser
            loser = user
            n_loser = n_user
            dice_loser = dice_user
            #End
            msg = "{} won ! And wins the amount of {}.".format(winner.mention, amount)
            bank.transfer_credits(loser, winner, amount)
            self.exp_up(winner, server)
        elif n_user > n_author:
            #Winner
            winner = user
            n_winner = n_user
            dice_winner = dice_user
            #Loser
            loser = author
            n_loser = n_author
            dice_loser = dice_author
            #End
            msg = "{} won ! And wins the amount of {}.".format(winner.mention, amount)
            bank.transfer_credits(loser, winner, amount)
            self.exp_up(winner, server)
        #Tie
        elif n_author == n_user:
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            loser = user
            n_loser = n_user
            dice_loser = dice_user
            msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, user.mention)
        dict_results = {"winner" : winner, "n_winner" : n_winner, "dice_winner" : dice_winner,
                        "loser" : loser, "n_loser" : n_loser, "dice_loser" : dice_loser, "msg" : msg}
        return dict_results

    @commands.group(name="idiceset", pass_context=True)
    @checks.is_owner()
    async def _idiceset(self, ctx):
        '''The differents configs for iDice.'''
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_idiceset.command(pass_context=True)
    @checks.is_owner()
    async def start(self, ctx):
        """To init the differents configs essentials."""
        user = ctx.message.author
        server = ctx.message.server
        if not self.config_exists(server):
            if not self.enough_emojis(server):
                await self.bot.say("You don't have enough places available in your server's emojis.\n"
                                   "The iDice Battle need 4 places available in your server's emojis.")
            else:
                await self.bot.say("It will take 4 places available in your server's emojis. Is it ok ? (y/n)")
                response = await self.bot.wait_for_message(timeout=60, author=user)
                if response == None:
                    await self.bot.say("You didn't answer to me, the configs steps are stopped.")
                elif response.content == 'y':
                    self.add_server_config(server)
                    await self.bot.say("The configs have been initialized.")
                elif response.content == 'n':
                    await self.bot.say("Ok then...\nThe configs steps are stopped.")
        else:
            await self.bot.say("Have you forgotten? The configs have already been initialized.")

    @commands.group(name="idice", pass_context=True)
    async def _idice(self, ctx):
        '''"Parce que c'est une très bonne iDé !"'''
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_idice.command(pass_context=True)
    async def register(self, ctx):
        """To create and iDice Profile."""
        author = ctx.message.author
        server = ctx.message.server
        try:
            account = self.create_profile(author, server)
            await self.bot.say("{}: iDice profile created :white_check_mark:!".format(author.mention))
        except AlreadyRegistered:
            await self.bot.say("{}, you already have an iDice profile.".format(author.mention))

    @_idice.command(pass_context=True)
    async def profile(self, ctx, user : discord.Member = None):
        """To see your (or someone else) iDice profile."""
        author = ctx.message.author
        server = ctx.message.server
        if user!=None:
            author = user
        try:
            data = discord.Embed(description="iDice Profile", color=author.color)
            data.set_author(name=author.display_name, icon_url=author.avatar_url)
            data.add_field(name="Level 🏆", value=self.get_lvl(author, server))
            data.add_field(name="Experience ⭐", value=self.get_exp(author, server))
            data.add_field(name="Bonus", value=self.get_bonus(author, server), inline=False)
            await self.bot.delete_message(ctx.message)
            await self.bot.say(embed=data)
        except:
            await self.bot.say("{} : You don't have an iDice profile. You have to do `{}idice register`.".format(author.mention, ctx.prefix))

    @_idice.command(pass_context=True)
    async def duel(self, ctx, user : discord.Member, amount : int):
        """To start an iDice duel."""
        author = ctx.message.author
        server = ctx.message.server
        bank = self.bot.get_cog("Economy").bank

        if not self.config_exists(server):
            await self.bot.delete_message(ctx.message)
            await self.bot.say("{} : The configs are not initialized yet, the bot owner needs to do `{}idiceset start`".format(author.mention, ctx.prefix))
        else:
            #No auto-duel
            if author == user:
                await self.bot.say("{} : You can't duel yourself.".format(author.mention))
            else:
                #Check bank.account_exists (positive response)
                if bank.account_exists(user) and bank.account_exists(author):
                    bankauthor = bank.get_balance(author)
                    bankuser = bank.get_balance(user)
                    #Check account != 0
                    if bankauthor == 0 or bankuser == 0:
                        await self.bot.delete_message(ctx.message)
                        await self.bot.say("{}: You or your opponent, has nothing in the bank account.\n"
                                           "Unable to proceed to an iDice duel.".format(author.mention))
                    else:
                        #Check bank.account >= amount
                        if bankauthor < amount or bankuser < amount:
                            await self.bot.delete_message(ctx.message)
                            await self.bot.say("{}: You or your opponent, don't have enough in his bank account.\n"
                                               "Unable to proceed to an iDice duel.".format(author.mention))
                        else:
                            #Check iDice Profile exists (positive response)
                            if self.profile_exists(user, server) and self.profile_exists(author, server):
                                #Start w/ wait_for_reaction
                                await self.bot.delete_message(ctx.message)
                                msg1 = await self.bot.say("{}, do you want to confront {} in an iDice duel, for an amount of {}?"
                                "".format(user.mention, author.mention, amount))
                                await self.bot.add_reaction(msg1, '\U00002705')
                                await self.bot.add_reaction(msg1, '\U0000274e')
                                rea = await self.bot.wait_for_reaction(['\U00002705', '\U0000274e'], user=user, timeout=30, message=msg1)
                                #No response
                                if rea == None:
                                    await self.bot.delete_message(msg1)
                                    await self.bot.say("{}: Your opponent didn't reply.".format(author.mention))
                                #Positive response
                                elif rea.reaction.emoji == '\U00002705':
                                    dict_dice_author = self.dice_author(author, server)
                                    dice_author = dict_dice_author["dice_author"]
                                    n_author = dict_dice_author["n_author"]
                                    dict_dice_user = self.dice_user(user, server)
                                    dice_user = dict_dice_user["dice_user"]
                                    n_user = dict_dice_user["n_user"]
                                    #Résults
                                    dict_results = self.results(author, user, n_author, n_user, dice_author, dice_user, bank, amount)
                                    winner = dict_results["winner"]
                                    n_winner = dict_results["n_winner"]
                                    dice_winner = dict_results["dice_winner"]
                                    loser = dict_results["loser"]
                                    n_loser = dict_results["n_loser"]
                                    dice_loser = dict_results["dice_loser"]
                                    msg = dict_results["msg"]
                                    #Viewing
                                    data = discord.Embed(description="iDice Duel :game_die: :crossed_swords:", color=author.color)
                                    data.add_field(name=winner.display_name, value="{} {} {}".format(dice_winner, n_winner, dice_winner))
                                    data.add_field(name=loser.display_name, value="{} {} {}".format(dice_loser, n_loser, dice_loser))
                                    await self.bot.delete_message(msg1)
                                    await self.bot.say(embed=data, content=msg)
                                    #Negative response
                                elif rea.reaction.emoji == '\U0000274e':
                                    await self.bot.delete_message(msg1)
                                    await self.bot.say("{} : Your opponent have no balls to confront you.".format(author.mention))
                            else:#Check iDice profile exists (Negative response)
                                await self.bot.delete_message(ctx.message)
                                await self.bot.say("{} : You or your opponent, doesn't have an iDice profile.\n"
                                                   "Unable to proceed to an iDice duel: someone have to do `{}idice register`.".format(author.mention, ctx.prefix))
                else:#Check bank.account_exists (Negative response)
                    await self.bot.delete_message(ctx.message)
                    await self.bot.say("{}: You or your opponent, doesn't have a bank account.\n"
                                       "Unable to proceed to an iDice duel.".format(author.mention))

def check_folders():
    folders = ("data", "data/iDice/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)

def check_profile():
    if not os.path.isfile("data/iDice/profile.json"):
        print("Creating empty profile.json...")
        dataIO.save_json("data/iDice/profile.json", {"servers" : {}})

def check_config():
    if not os.path.isfile("data/iDice/config.json"):
        print("Creating empty config.json...")
        dataIO.save_json("data/iDice/config.json", {"servers" : {}})

def setup(bot):
    check_folders()
    check_profile()
    check_config()
    bot.add_cog(IDiceBattle(bot))
