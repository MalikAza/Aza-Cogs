#cog.name inspired by Hitsumo
#Idée développée par Aza' & Hitsumo
#cog codé par Aza'
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
        self.file_path = "data/iDice/attributs.json"
        self.idice = dataIO.load_json(self.file_path)

    def create_attributs(self, user):
        if not self.attributs_exists(user):
            attributs = {"lvl": 1,
                         "exp" : 0,
                         "supps" : 0
                         }
            self.idice[user.id] = attributs
            self._save_attributs()
        else:
            raise AlreadyRegistered()

    def attributs_exists(self, user):
        try:
            self._get_attributs(user)
        except NotRegistered:
            return False
        return True

    def get_lvl(self, user):
        attributs = self._get_attributs(user)
        return attributs["lvl"]

    def get_exp(self, user):
        attributs = self._get_attributs(user)
        return attributs["exp"]

    def exp_up(self, user):
        attributs = self._get_attributs(user)
        exp = attributs["exp"]
        lvl = attributs["lvl"]
        possible_futur_exp = (exp + 1)
        if possible_futur_exp > (10*lvl):
            self.lvl_up(user)
        else:
            attributs["exp"] += 1
            self.idice[user.id] = attributs
            self._save_attributs()

    def get_supps(self, user):
        attributs = self._get_attributs(user)
        return attributs["supps"]

    def lvl_up(self, user):
        attributs = self._get_attributs(user)
        attributs["lvl"] += 1
        attributs["exp"] = 0
        attributs["supps"] += 1
        self.idice[user.id] = attributs
        self._save_attributs()

    def _save_attributs(self):
        dataIO.save_json("data/iDice/attributs.json", self.idice)

    def _get_attributs(self, user):
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
        """Pour enregistrer votre compte iDice."""
        author = ctx.message.author
        try:
            account = self.create_attributs(author)
            await self.bot.say("{} : Profile iDice créé :white_check_mark: !".format(author.mention))
        except AlreadyRegistered:
            await self.bot.say("{}, tu as déjà un profile iDice.".format(author.mention))

    @_idice.command(pass_context=True)
    async def profile(self, ctx, user : discord.Member = None):
        """Pour savoir votre profile iDice. (indisponible actuellement)"""
        author = ctx.message.author
        if user!=None:
            author = user
        data = discord.Embed(description="iDice Profile", color=author.color)
        data.set_author(name=author.display_name, icon_url=author.avatar_url)
        data.add_field(name="Niveau 🏆", value= self.get_lvl(author))
        data.add_field(name="Expérience ⭐", value=self.get_exp(author))
        data.add_field(name="Bonus", value=self.get_supps(author), inline=False)
        await self.bot.delete_message(ctx.message)
        await self.bot.say(embed=data)

    @_idice.command(pass_context=True)
    async def duel(self, ctx, user : discord.Member, amount : int):
        """Pour lancer un duel iDice."""
        author = ctx.message.author
        server = ctx.message.server
        bank = self.bot.get_cog("Economy").bank

        #Anti auto-duel
        if author == user:
            await self.bot.say("{} : Vous ne pouvez pas vous affronter vous même.".format(author.mention))
        else:
            #Check bank.account_exists (positif)
            if bank.account_exists(user) and bank.account_exists(author):
                bankauthor = dataIO.load_json("data/economy/bank.json")[server.id][author.id]["balance"]
                bankuser = dataIO.load_json("data/economy/bank.json")[server.id][user.id]["balance"]
                #Check account != 0
                if bankauthor == 0 or bankuser == 0:
                    await self.bot.delete_message(ctx.message)
                    await self.bot.say("{} : Toi ou l'autre participant, n'as rien dans son compte en banque.\n"
                                       "Impossible de faire un iDice duel.".format(author.mention))
                else:
                    #Check account suffisant
                    if bankauthor < amount or bankuser < amount:
                        await self.bot.delete_message(ctx.message)
                        await self.bot.say("{} : Toi ou l'autre participant, n'as pas assez dans son compte en banque.\n"
                                           "Impossible de faire un iDice duel.".format(author.mention))
                    else:
                        #Check iDice Profile existant (positif)
                        if self.attributs_exists(user) and self.attributs_exists(author):
                            #Début w/ Réa
                            await self.bot.delete_message(ctx.message)
                            msg1 = await self.bot.say("{}, voulez vous affronter {} en iDice duel, pour la somme de {} crédits ?"
                            "".format(user.mention, author.mention, amount))
                            await self.bot.add_reaction(msg1, '\U00002705')
                            await self.bot.add_reaction(msg1, '\U0000274e')
                            rea = await self.bot.wait_for_reaction(['\U00002705', '\U0000274e'], user=user, timeout=30, message=msg1)
                            #Pas de réponses
                            if rea == None:
                                await self.bot.delete_message(msg1)
                                await self.bot.say("{} : Ton adversaire n'as pas répondu à la demande de iDice duel.".format(author.mention))
                            #Réponse positive (Réaction prise en compte, mais ne continue pas.)
                            elif rea.reaction.emoji == '\U00002705':
                                msg = ""
                                gagnant = ""
                                perdant = ""
                                échec_crit = "<:roll_echec_crit:367296625799856128> "
                                échec = "<:roll_echec:367296637825056779> "
                                normal = ":game_die: "
                                réussite_crit = "<:roll_reussite:367296651058085888> "
                                supps_author = self.get_supps(author) #Testez si la fonction marche
                                supps_user = self.get_supps(user)
                                #Dice_Author
                                n1_author = randint(1, 10)
                                if n1_author == 10:#Réussite_crit
                                    n2_author = randint(1, 10)
                                    n_author = n1_author + n2_author
                                    dice_author = réussite_crit
                                    supps_author = supps_author + int((0.50*supps_author))
                                    if supps_author != 0:
                                        n_author = n_author + supps_author
                                elif n1_author == 1:#Echec
                                    n2_author = randint(1, 10)
                                    n_author = n1_author + n2_author
                                    if n2_author == 1:#Echec_crit
                                        dice_author = échec_crit
                                    else:#Echec (suite)
                                        dice_author = échec
                                        supps_author = supps_author - int((0.25*supps_author))
                                    if supps_author != 0:
                                        n_author = n_author + supps_author
                                        supps_author = supps_author - int((0.50*supps_author))
                                elif n1_author != 10 and n1_author != 1:#Normal
                                    dice_author = normal
                                    n_author = n1_author
                                    if supps_author != 0:
                                        n_author = n_author + supps_author
                                #Dice_User
                                n1_user = randint(1, 10)
                                if n1_user == 10:#Réussite_crit
                                    n2_user = randint(1, 10)
                                    n_user = n1_user + n2_user
                                    dice_user = réussite_crit
                                    supps_user = supps_user + int((0.50*supps_user))
                                    if supps_user != 0:
                                        n_user = n_user + supps_user
                                elif n1_user == 1:#Echec
                                    n2_user = randint(1, 10)
                                    n_user = n1_user + n2_user
                                    if n2_user == 1:#Echec_crit
                                        dice_user = échec_crit
                                    else:#Echec (suite)
                                        dice_user = échec
                                        supps_user = supps_user - int((0.25*supps_user))
                                    if supps_user != 0:
                                        n_user = n_user + supps_user
                                        supps_user = supps_user - int((0.50*supps_user))
                                elif n1_user != 10 and n1_user != 1:#Normal
                                    dice_user = normal
                                    n_user = n1_user
                                    if supps_user != 0:
                                        n_user = n_user + supps_user
                                #Résultats
                                if n_author > n_user:
                                    #gagnant
                                    gagnant = author
                                    n_gagnant = n_author
                                    dice_gagnant = dice_author
                                    #perdant
                                    perdant = user
                                    n_perdant = n_user
                                    dice_perdant = dice_user
                                    #End
                                    msg = "{} a gagné ! Et remporte donc la somme de {} crédits.".format(gagnant.mention, amount)
                                    bank.transfer_credits(perdant, gagnant, amount)
                                    self.exp_up(gagnant)
                                elif n_user > n_author:
                                    #gagnant
                                    gagnant = user
                                    n_gagnant = n_user
                                    dice_gagnant = dice_user
                                    #perdant
                                    perdant = author
                                    n_perdant = n_author
                                    dice_perdant = dice_author
                                    #End
                                    msg = "{} a gagné ! Et remporte donc la somme de {} crédits.".format(gagnant.mention, amount)
                                    bank.transfer_credits(perdant, gagnant, amount)
                                    self.exp_up(gagnant)
                                #Egalité
                                elif n_author == n_user:
                                    gagnant = author
                                    n_gagnant = n_author
                                    dice_gagnant = dice_author
                                    perdant = user
                                    n_perdant = n_user
                                    dice_perdant = dice_user
                                    msg = "{} & {} : Egalité ! Personne ne gagne, personne ne perds.".format(author.mention, user.mention)
                                #Affichage
                                data = discord.Embed(description="iDice Duel :game_die: :crossed_swords:", color=author.color)
                                data.add_field(name=gagnant.display_name, value="{} {} {}".format(dice_gagnant, n_gagnant, dice_gagnant))
                                data.add_field(name=perdant.display_name, value="{} {} {}".format(dice_perdant, n_perdant, dice_perdant))
                                await self.bot.delete_message(msg1)
                                await self.bot.say(embed=data, content=msg)
                                #Réponse négative
                            elif rea.reaction.emoji == '\U0000274e':
                                await self.bot.delete_message(msg1)
                                await self.bot.say("{} : Dommage, mais ton adversaire n'as pas les couilles de t'affronter.".format(author.mention))
                        else:#Check iDice Profile existant (négatif)
                            await self.bot.delete_message(ctx.message)
                            await self.bot.say("{} : Toi ou l'autre participant, n'as pas de profile iDice.\n"
                                               "Impossible de faire un iDice duel : pensez à faire la commande `[p]idice register`.".format(author.mention))
            else:#Check bank.account_exists (négatif)
                await self.bot.delete_message(ctx.message)
                await self.bot.say("{} : Toi ou l'autre participant, n'as pas de compte en banque.\n"
                                   "Impossible de faire un iDice duel.".format(author.mention))

def check_folders():
    folders = ("data", "data/iDice/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)

def check_files():
    if not os.path.isfile("data/iDice/attributs.json"):
        print("Creating empty attributs.json...")
        dataIO.save_json("data/iDice/attributs.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(IDiceBattle(bot))
