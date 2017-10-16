#cog.name inspired by Hitsumo
#Idea developped by Aza' & Hitsumo
#cog coding par Aza'
import discord
from discord.ext import commands
from random import randint
from cogs.utils.dataIO import dataIO
from copy import deepcopy
from __main__ import send_cmd_help
import os
import logging
import asyncio

class IDiceError(Exception):
    pass

class AlreadyRegistered(IDiceError):
    pass

class NotRegistered(IDiceError):
    pass

class IDiceBattle:
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/iDice/profile.json"
        self.idice = dataIO.load_json(self.file_path)

    def create_profile(self, user):
        if not self.profile_exists(user):
            profile = {"lvl": 1,
                         "exp" : 0,
                         "bonus" : 0
                         }
            self.idice[user.id] = profile
            self._save_profile()
        else:
            raise AlreadyRegistered()

    def profile_exists(self, user):
        try:
            self._get_profile(user)
        except NotRegistered:
            return False
        return True

    def get_lvl(self, user):
        profile = self._get_profile(user)
        return profile["lvl"]

    def get_exp(self, user):
        profile = self._get_profile(user)
        return profile["exp"]

    def exp_up(self, user):
        profile = self._get_profile(user)
        exp = profile["exp"]
        lvl = profile["lvl"]
        possible_futur_exp = (exp + 1)
        if possible_futur_exp > (10*lvl):
            self.lvl_up(user)
        else:
            profile["exp"] += 1
            self.idice[user.id] = profile
            self._save_profile()

    def get_bonus(self, user):
        profile = self._get_profile(user)
        return profile["bonus"]

    def lvl_up(self, user):
        profile = self._get_profile(user)
        profile["lvl"] += 1
        profile["exp"] = 0
        profile["bonus"] += 1
        self.idice[user.id] = profile
        self._save_profile()

    def _save_profile(self):
        dataIO.save_json("data/iDice/profile.json", self.idice)

    def _get_profile(self, user):
        try:
            return deepcopy(self.idice[user.id])
        except KeyError:
            raise NotRegistered()

    @commands.group(name="idice", pass_context=True)
    async def _idice(self, ctx):
        '''"Parce que c'est une très bonne iDé !"'''
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_idice.command(pass_context=True)
    async def register(self, ctx):
        """To create and iDice Profile."""
        author = ctx.message.author
        try:
            account = self.create_profile(author)
            await self.bot.say("{}: iDice profile created :white_check_mark:!".format(author.mention))
        except AlreadyRegistered:
            await self.bot.say("{}, you already have an iDice profile.".format(author.mention))

    @_idice.command(pass_context=True)
    async def profile(self, ctx, user : discord.Member = None):
        """To see your (or someone else) iDice profile."""
        author = ctx.message.author
        if user!=None:
            author = user
        data = discord.Embed(description="iDice Profile", color=author.color)
        data.set_author(name=author.display_name, icon_url=author.avatar_url)
        data.add_field(name="Level 🏆", value= self.get_lvl(author))
        data.add_field(name="Experience ⭐", value=self.get_exp(author))
        data.add_field(name="Bonus", value=self.get_bonus(author), inline=False)
        await self.bot.delete_message(ctx.message)
        await self.bot.say(embed=data)

    @_idice.command(pass_context=True)
    async def duel(self, ctx, user : discord.Member, amount : int):
        """To start an iDice duel."""
        author = ctx.message.author
        server = ctx.message.server
        bank = self.bot.get_cog("Economy").bank

        #No auto-duel
        if author == user:
            await self.bot.say("{} : You can't duel yourself.".format(author.mention))
        else:
            #Check bank.account_exists (positive response)
            if bank.account_exists(user) and bank.account_exists(author):#Raw retrieving data because of some bugs in the past (have to be retry)
                bankauthor = dataIO.load_json("data/economy/bank.json")[server.id][author.id]["balance"]
                bankuser = dataIO.load_json("data/economy/bank.json")[server.id][user.id]["balance"]
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
                        if self.profile_exists(user) and self.profile_exists(author):
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
                                msg = ""
                                winner = ""
                                loser = ""
                                crit_failure = "<:roll_echec_crit:367296625799856128> "
                                failure = "<:roll_echec:367296637825056779> "
                                normal = ":game_die: "
                                crit_success = "<:roll_reussite:367296651058085888> "
                                bonus_author = self.get_bonus(author)
                                bonus_user = self.get_bonus(user)
                                #Dice_Author
                                n1_author = randint(1, 10)
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
                                        dice_author = crit_failure
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
                                #Dice_User
                                n1_user = randint(1, 10)
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
                                #Résults
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
                                    self.exp_up(winner)
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
                                    self.exp_up(winner)
                                #Tie
                                elif n_author == n_user:
                                    winner = author
                                    n_winner = n_author
                                    dice_winner = dice_author
                                    loser = user
                                    n_loser = n_user
                                    dice_loser = dice_user
                                    msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, user.mention)
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
                                               "Unable to proceed to an iDice duel: someone have to do `{}idice register`.".format(ctx.prefix, author.mention))
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
        dataIO.save_json("data/iDice/profile.json", {})

def setup(bot):
    check_folders()
    check_profile()
    bot.add_cog(IDiceBattle(bot))
