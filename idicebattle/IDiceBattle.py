#cog.name inspired by Hitsumo
#Idea developped by Aza' & Hitsumo
#cog coding by Aza'
#converted in V3 by Aza'
#wanting to burn it all during the convertion by Aza'
from redbot.core import commands, checks, Config, bank
from random import randint
import discord
import asyncio

class IDiceBattle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier='2110932804290696')
        default_profile = {
            "lvl": 1,
            "exp": 0,
            "bonus": 0
        }
        self.config.register_member(**default_profile)

    async def exp_up(self, user):
        exp = await self.config.member(user).exp()
        lvl = await self.config.member(user).lvl()
        bonus = await self.config.member(user).bonus()
        possible_futur_exp = (exp + 10)
        #exp_up + lvl_up
        if possible_futur_exp >= (10*lvl):
            #lvl_up
            await self.config.member(user).lvl.set(lvl + 1)
            #reset exp
            await self.config.member(user).exp.set(0)
            #bonus_up
            await self.config.member(user).bonus.set(bonus + 1)
            return "ylvlup"
        #Normal exp_up
        else:
            await self.config.member(user).exp.set(exp + 10)
            return "nlvlup"

    async def exp_up_vs_bot(self, user):
        exp = await self.config.member(user).exp()
        lvl = await self.config.member(user).lvl()
        bonus = await self.config.member(user).bonus()
        possible_futur_exp = (exp + 1)
        #exp_up + lvl_up
        if possible_futur_exp >= (10*lvl):
            #lvl_up
            await self.config.member(user).lvl.set(lvl + 1)
            #reset exp
            await self.config.member(user).exp.set(0)
            #bonus_up
            await self.config.member(user).bonus.set(bonus + 1)
            return "ylvlup"
        #Normal exp_up
        else:
            await self.config.member(user).exp.set(exp + 1)
            return "nlvlup"

    def dice_author(self, author, bonus_author):
        crit_failure = self.bot.get_emoji(380852648213217290)
        failure = self.bot.get_emoji(380852671273500683)
        normal = self.bot.get_emoji(380852681364865034)
        crit_success = self.bot.get_emoji(380852660259127297)
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

    def dice_user(self, user, bonus_user):
        crit_failure = self.bot.get_emoji(380852648213217290)
        failure = self.bot.get_emoji(380852671273500683)
        normal = self.bot.get_emoji(380852681364865034)
        crit_success = self.bot.get_emoji(380852660259127297)
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
        dict_dice_user = {"dice_user" : dice_user, "n_user" : n_user}
        return dict_dice_user

    def dice_bot(self, author, bonus_author):
        crit_failure = self.bot.get_emoji(380852648213217290)
        failure = self.bot.get_emoji(380852671273500683)
        normal = self.bot.get_emoji(380852681364865034)
        crit_success = self.bot.get_emoji(380852660259127297)
        n1_bot = randint(1, 10)
        bonus_bot = int(1.5*bonus_author)
        if n1_bot == 10:#Critical success
            n2_bot = randint(1, 10)
            n_bot = n1_bot + n2_bot
            dice_bot = crit_success
            bonus_bot = bonus_bot + int((0.50*bonus_bot))
            if bonus_bot != 0:
                n_bot = n_bot + bonus_bot
        elif n1_bot == 1:#Failure
            n2_bot = randint(1, 10)
            n_bot = n1_bot + n2_bot
            if n2_bot == 1:#Critical failure
                dice_bot = crit_failure
            else:#Failure (following)
                dice_bot = failure
                bonus_bot = bonus_bot - int((0.25*bonus_bot))
            if bonus_bot != 0:
                n_bot = n_bot + bonus_bot
                bonus_bot = bonus_bot - int((0.50*bonus_bot))
        elif n1_bot != 10 and n1_bot != 1:#Normal
            dice_bot = normal
            n_bot = n1_bot
            if bonus_bot != 0:
                n_bot = n_bot + bonus_bot
        dict_dice_bot = {"dice_bot" : dice_bot, "n_bot" : n_bot}
        return dict_dice_bot

    @commands.group()
    @commands.guild_only()
    async def idice(self, ctx):
        '''"Parce que c'est une très bonne iDé !"'''

    @idice.command(name="profile")
    @commands.guild_only()
    async def idice_profile(self, ctx, user : discord.Member = None):
        """To see your (or someone else) iDice profile."""
        author = ctx.author
        if user != None:
            author = user
        data = discord.Embed(description="iDice Profile", color=author.color)
        data.set_author(name=author.display_name, icon_url=author.avatar_url)
        data.add_field(name="Level 🏆", value = await self.config.member(author).lvl())
        data.add_field(name="Experience ⭐", value = await self.config.member(author).exp())
        data.add_field(name="Bonus", value = await self.config.member(author).bonus(), inline=False)
        await ctx.message.delete()
        await ctx.send(embed=data)

    @idice.command(name="duel")
    @commands.guild_only()
    async def idice_duel(self, ctx, user : discord.Member, amount : int):
        """To start an iDice duel."""
        author = ctx.author
        #No auto-duel
        if author == user:
            await ctx.send("{} : You can't duel yourself.".format(author.mention))
        else:
            #Check account.can_spend() | positive response
            if await bank.can_spend(author, amount) and await bank.can_spend(user, amount):
                #Start w/ wait_for_reaction
                await ctx.message.delete()
                msg1 = await ctx.send("{}, do you want to confront {} in an iDice duel, for an amount of {}?"
                "".format(user.mention, author.mention, amount))
                await msg1.add_reaction('✅')
                await msg1.add_reaction('❌')
                try:
                    def check(reaction, opponent):
                        return opponent == user and (reaction.emoji == '✅' or reaction.emoji == '❌')

                    reaction, opponent = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    #Positive response
                    if reaction.emoji == '✅':
                        author_bonus = await self.config.member(author).bonus()
                        user_bonus = await self.config.member(user).bonus()
                        dict_dice_author = self.dice_author(author, author_bonus)
                        dice_author = dict_dice_author["dice_author"]
                        n_author = dict_dice_author["n_author"]
                        dict_dice_user = self.dice_user(user, user_bonus)
                        dice_user = dict_dice_user["dice_user"]
                        n_user = dict_dice_user["n_user"]
                        #Results
                        #Because of the fucking coroutines I can't return a fucking dict out of a coroutined function
                        #So have fun and have a function in a command, having then an ugly 5billions lines command
                        #Fuck you python
                        msg = ""
                        winner = ""
                        loser = ""
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
                            await bank.transfer_credits(loser, winner, amount)
                            self_exp_up = await self.exp_up(winner)
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
                            await bank.transfer_credits(loser, winner, amount)
                            self_exp_up = await self.exp_up(winner)
                        #Tie
                        elif n_author == n_user:
                            winner = author
                            n_winner = n_author
                            dice_winner = dice_author
                            loser = user
                            n_loser = n_user
                            dice_loser = dice_user
                            msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, user.mention)
                            self_exp_up = "nlvlup"
                        #Viewing
                        data = discord.Embed(description="iDice Duel <:normal_dice:380852681364865034> :crossed_swords:", color=author.color)
                        data.add_field(name=winner.display_name, value="{} {} {}".format(dice_winner, n_winner, dice_winner))
                        data.add_field(name=loser.display_name, value="{} {} {}".format(dice_loser, n_loser, dice_loser))
                        await msg1.delete()
                        await ctx.send(embed=data, content=msg)
                        #Check if leveled up
                        if self_exp_up == "ylvlup":
                            lvl_winner = await self.config.member(winner).lvl()
                            await ctx.send("{} has leveled up to {} ! Congrats !!!".format(winner.mention, lvl_winner))
                    #Negative response
                    if reaction.emoji == '❌':
                        await msg1.delete()
                        await ctx.send("{} : Your opponent have no balls to confront you.".format(author.mention))
                #No response
                except asyncio.TimeoutError:
                    await msg1.delete()
                    await ctx.send("{}: Your opponent didn't reply.".format(author.mention))
            #author can't spend
            elif not await bank.can_spend(author, amount):
                await ctx.message.delete()
                return await ctx.send("{}: You don't have enough in your bank account.\n"
                                      "Unable to proceed to an iDice duel.".format(author.mention))
            #user can't spend
            elif not await bank.can_spend(user, amount):
                await ctx.message.delete()
                return await ctx.send("{}: Your opponent don't have enough in his/her bank account.\n"
                                      "Unable to proceed to an iDice duel.".format(author.mention))

#From here, 'Kaine' is a retard. He ask me to write down 'penis', so here it is : PENIS.

    @idice.command(name="pve")
    @commands.guild_only()
    async def idice_pve(self, ctx):
        """To start an iDice duel VS the bot."""
        author = ctx.author
        bot = self.bot.user
        author_bonus = await self.config.member(author).bonus()

        #Start
        dict_dice_author = self.dice_author(author, author_bonus)
        dice_author = dict_dice_author["dice_author"]
        n_author = dict_dice_author["n_author"]
        dict_dice_bot = self.dice_bot(author, author_bonus)
        dice_bot = dict_dice_bot["dice_bot"]
        n_bot = dict_dice_bot["n_bot"]
        #Results
        #Because of the fucking coroutines I can't return a fucking dict out of a coroutined function
        #So have fun and have a function in a command, having then an ugly 5billions lines command
        #Fuck you python
        msg = ""
        winner = ""
        loser = ""
        if n_author > n_bot:
            #Winner
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            #Loser
            loser = bot
            n_loser = n_bot
            dice_loser = dice_bot
            #End
            msg = "{} won !".format(winner.mention)
            self_exp_up = await self.exp_up_vs_bot(winner)
        elif n_bot > n_author:
            #Winner
            winner = bot
            n_winner = n_bot
            dice_winner = dice_bot
            #Loser
            loser = author
            n_loser = n_author
            dice_loser = dice_author
            #End
            msg = "{} won !".format(winner.mention)
            self_exp_up = "nlvlup"
        #Tie
        elif n_author == n_bot:
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            loser = bot
            n_loser = n_bot
            dice_loser = dice_bot
            msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, bot.mention)
            self_exp_up = "nlvlup"
        #Viewing
        data = discord.Embed(description="iDice Duel <:normal_dice:380852681364865034> :crossed_swords:", color=author.color)
        data.add_field(name=winner.display_name, value="{} {} {}".format(dice_winner, n_winner, dice_winner))
        data.add_field(name=loser.display_name, value="{} {} {}".format(dice_loser, n_loser, dice_loser))
        await ctx.message.delete()
        await ctx.send(embed=data, content=msg)
        #Check if leveled up
        if self_exp_up == "ylvlup":
            lvl_winner = await self.config.member(winner).lvl()
            await ctx.send("{} has leveled up to {} ! Congrats !!!".format(winner.mention, lvl_winner))
