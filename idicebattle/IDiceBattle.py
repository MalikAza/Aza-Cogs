# cog.name inspired by Hitsumo
# Idea developed by Aza' & Hitsumo
# cog coding by Aza' & RissCrew
# converted in V3 by Aza'
# wanting to burn it all during the conversion by Aza'
from redbot.core import commands, Config, bank, checks
from random import randint
from io import BytesIO
import discord
import asyncio
import matplotlib.pyplot as plt

'''
Those are url for the emojis:

crit_failure: https://i.imgur.com/paUn18x.png
failure: https://i.imgur.com/ZlUJv2a.png
normal_dice: https://i.imgur.com/BJ3nNtA.png
crit_success: https://i.imgur.com/KRO8zMD.png
'''

def enough_emojis(server):
    nbr_emoji = 0
    for emoji in server.emojis:
        if not emoji.animated:
            nbr_emoji += 1
    if nbr_emoji <= 46:
        return True
    else:
        return False


class IDiceBattle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2110932804290696)
        default_profile = {
            "lvl": 1,
            "exp": 0,
            "bonus": 0
        }
        self.config.register_member(**default_profile)
        self.config.register_guild(config=False)

    async def exp_up(self, user):
        exp = await self.config.member(user).exp()
        lvl = await self.config.member(user).lvl()
        bonus = await self.config.member(user).bonus()
        possible_futur_exp = (exp + 10)
        # exp_up + lvl_up
        if possible_futur_exp >= (10 * lvl):
            # lvl_up
            await self.config.member(user).lvl.set(lvl + 1)
            # reset exp
            await self.config.member(user).exp.set(0)
            # bonus_up
            await self.config.member(user).bonus.set(bonus + 1)
            return "ylvlup"
        # Normal exp_up
        else:
            await self.config.member(user).exp.set(exp + 10)
            return "nlvlup"

    async def exp_up_vs_bot(self, user):
        exp = await self.config.member(user).exp()
        lvl = await self.config.member(user).lvl()
        bonus = await self.config.member(user).bonus()
        possible_futur_exp = (exp + 1)
        # exp_up + lvl_up
        if possible_futur_exp >= (10 * lvl):
            # lvl_up
            await self.config.member(user).lvl.set(lvl + 1)
            # reset exp
            await self.config.member(user).exp.set(0)
            # bonus_up
            await self.config.member(user).bonus.set(bonus + 1)
            return "ylvlup"
        # Normal exp_up
        else:
            await self.config.member(user).exp.set(exp + 1)
            return "nlvlup"

    def dice_author(self, bonus_author):
        return self.dice(bonus_user=bonus_author, dict_user="dice_author", dict_n_user="n_author")

    def dice_user(self, bonus_user):
        return self.dice(bonus_user=bonus_user, dict_user="dice_user", dict_n_user="n_user")

    def dice_bot(self, bonus_author):
        return self.dice(bonus_user=int(1.5 * bonus_author), dict_user="dice_bot", dict_n_user="n_bot")

    def dice(self, bonus_user, dict_user, dict_n_user):
        crit_failure = self.bot.get_emoji(380852648213217290)
        failure = self.bot.get_emoji(380852671273500683)
        normal = self.bot.get_emoji(380852681364865034)
        crit_success = self.bot.get_emoji(380852660259127297)
        n1_user = randint(1, 10)
        if n1_user == 10:  # Critical success
            n2_user = randint(1, 10)
            n_user = n1_user + n2_user
            dice_user = crit_success
            bonus_user = bonus_user + int((0.50 * bonus_user))
            if bonus_user != 0:
                n_user = n_user + bonus_user
        elif n1_user == 1:  # Failure
            n2_user = randint(1, 10)
            n_user = n1_user + n2_user
            if n2_user == 1:  # Critical failure
                dice_user = crit_failure
            else:  # Failure (following)
                dice_user = failure
                bonus_user = bonus_user - int((0.25 * bonus_user))
            if bonus_user != 0:
                n_user = n_user + bonus_user
        else:  # Normal
            dice_user = normal
            n_user = n1_user
            if bonus_user != 0:
                n_user = n_user + bonus_user
        dict_dice_user = {dict_user: dice_user, dict_n_user: n_user}
        return dict_dice_user

    @commands.group()
    @commands.guild_only()
    async def idiceset(self, ctx):
        """The differents configs for iDice."""

    @idiceset.command(name="emoji")
    @commands.guild_only()
    async def idiceset_emoji(self, ctx):
        """Install the essentials emojis."""
        author = ctx.author
        server = ctx.guild
        # Checking if this command has already been used
        if not await self.config.guild(server):
            # Checking if there is enough emojis slot in the server
            if not await enough_emojis(server):
                # Not enough slot
                await ctx.send("You don't have enough places available in your server's emojis.\n"
                               "The iDice Battle need 4 places available in your server's emojis.")
            else:  # Enough slot and asking if it's ok to create
                msg = ctx.send("It will take 4 places available in your server's emojis. Is it ok ?")
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                try:
                    def check(reaction, user):
                        return user == author and (reaction.emoji == '✅' or reaction.emoji == '❌')

                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    # Positive response
                    if reaction.emoji == '✅':
                        await ctx.send("The configs have been initialized.")

                        # We need to create the 4 emojis in the server right here
                        # Maybe an external (of this command) function ?

                        await self.config.guild(server).config.set(True)
                    # Negative response
                    if reaction.emoji == '❌':
                        await ctx.send("Ok then...\nThe configs steps are stopped.")
                # No response
                except asyncio.TimeoutError:
                    await ctx.send("You didn't answer to me, the configs steps are stopped.")
        # Command has already been used
        else:
            await ctx.send("Have you forgotten? The configs have already been initialized.")

    @commands.group()
    @commands.guild_only()
    async def idice(self, ctx):
        """"Parce que c'est une très bonne iDé !\""""

    @idice.command(name="profile")
    @commands.guild_only()
    async def idice_profile(self, ctx, user: discord.Member = None):
        """To see your (or someone else) iDice profile."""
        author = ctx.author
        if user is not None:
            author = user
        if author != self.bot.user:# Checking if bot
            data = discord.Embed(description="iDice Profile",
                                 color=author.color)
            data.set_author(name=author.display_name, icon_url=author.avatar_url)
            data.add_field(name="Level 🏆", value=await self.config.member(author).lvl())
            data.add_field(name="Experience ⭐", value=await self.config.member(author).exp())
            data.add_field(name="Bonus", value=await self.config.member(author).bonus(), inline=False)
            await ctx.message.delete()
            await ctx.send(embed=data)
        else:# No bot profile
            await ctx.send("I don't have any profile. Sorry not sorry but I'm the god of this game.")

    @idice.command(name="duel")
    @commands.guild_only()
    async def idice_duel(self, ctx, user: discord.Member, amount: int):
        """To start an iDice duel."""
        author = ctx.author
        # No auto-duel
        if author == user:
            await ctx.send("{} : You can't duel yourself.".format(author.mention))
        # No bot duel
        elif user == self.bot.user:
            await ctx.send("{} : Try to use `{}idice pve` instead.")
        else:
            # Check account.can_spend() | positive response
            if await bank.can_spend(author, amount) and await bank.can_spend(user, amount):
                # Start w/ wait_for_reaction
                await ctx.message.delete()
                msg1 = await ctx.send("{}, do you want to confront {} in an iDice duel, for an amount of {}?"
                                      "".format(user.mention, author.mention, amount))
                await msg1.add_reaction('✅')
                await msg1.add_reaction('❌')
                try:
                    def check(reaction, opponent):
                        return opponent == user and (reaction.emoji == '✅' or reaction.emoji == '❌')

                    reaction, opponent = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    # Positive response
                    if reaction.emoji == '✅':
                        author_bonus = await self.config.member(author).bonus()
                        user_bonus = await self.config.member(user).bonus()
                        dict_dice_author = self.dice_author(author_bonus)
                        dice_author = dict_dice_author["dice_author"]
                        n_author = dict_dice_author["n_author"]
                        dict_dice_user = self.dice_user(user_bonus)
                        dice_user = dict_dice_user["dice_user"]
                        n_user = dict_dice_user["n_user"]
                        # Results
                        # Because of the fucking coroutines I can't return a fucking dict out of a coroutine function
                        # So have fun and have a function in a command, having then an ugly 5billions lines command
                        # Fuck you python
                        if n_author != n_user:
                            if n_author > n_user:
                                # Winner
                                winner = author
                                n_winner = n_author
                                dice_winner = dice_author
                                # Loser
                                loser = user
                                n_loser = n_user
                                dice_loser = dice_user
                                # End
                            else:
                                # Winner
                                winner = user
                                n_winner = n_user
                                dice_winner = dice_user
                                # Loser
                                loser = author
                                n_loser = n_author
                                dice_loser = dice_author
                            # End
                            msg = "{} won ! And wins the amount of {}.".format(winner.mention, amount)
                            await bank.transfer_credits(loser, winner, amount)
                            self_exp_up = await self.exp_up(winner)
                        # Tie
                        else:
                            winner = author
                            n_winner = n_author
                            dice_winner = dice_author
                            loser = user
                            n_loser = n_user
                            dice_loser = dice_user
                            msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, user.mention)
                            self_exp_up = "nlvlup"
                        # Viewing
                        data = discord.Embed(
                            description="iDice Duel <:normal_dice:380852681364865034> :crossed_swords:",
                            color=author.color)
                        data.add_field(name=winner.display_name,
                                       value="{} {} {}".format(dice_winner, n_winner, dice_winner))
                        data.add_field(name=loser.display_name,
                                       value="{} {} {}".format(dice_loser, n_loser, dice_loser))
                        await msg1.delete()
                        await ctx.send(embed=data, content=msg)
                        # Check if leveled up
                        if self_exp_up == "ylvlup":
                            lvl_winner = await self.config.member(winner).lvl()
                            await ctx.send("{} has leveled up to {} ! Congrats !!!".format(winner.mention, lvl_winner))
                    # Negative response
                    if reaction.emoji == '❌':
                        await msg1.delete()
                        await ctx.send("{} : Your opponent have no balls to confront you.".format(author.mention))
                # No response
                except asyncio.TimeoutError:
                    await msg1.delete()
                    await ctx.send("{}: Your opponent didn't reply.".format(author.mention))
            # author can't spend
            elif not await bank.can_spend(author, amount):
                await ctx.message.delete()
                return await ctx.send("{}: You don't have enough in your bank account.\n"
                                      "Unable to proceed to an iDice duel.".format(author.mention))
            # user can't spend
            elif not await bank.can_spend(user, amount):
                await ctx.message.delete()
                return await ctx.send("{}: Your opponent don't have enough in his/her bank account.\n"
                                      "Unable to proceed to an iDice duel.".format(author.mention))

    # From here, 'Kaine' is a retard. He ask me to write down 'penis', so here it is : PENIS.

    @idice.command(name="pve")
    @commands.guild_only()
    async def idice_pve(self, ctx):
        """To start an iDice duel VS the bot."""
        author = ctx.author
        bot = self.bot.user
        author_bonus = await self.config.member(author).bonus()

        # Start
        dict_dice_author = self.dice_author(author_bonus)
        dice_author = dict_dice_author["dice_author"]
        n_author = dict_dice_author["n_author"]
        dict_dice_bot = self.dice_bot(author_bonus)
        dice_bot = dict_dice_bot["dice_bot"]
        n_bot = dict_dice_bot["n_bot"]
        # Results
        # Because of the fucking coroutines I can't return a fucking dict out of a coroutine function
        # So have fun and have a function in a command, having then an ugly 5billions lines command
        # Fuck you python
        if n_author > n_bot:
            # Winner
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            # Loser
            loser = bot
            n_loser = n_bot
            dice_loser = dice_bot
            # End
            msg = "{} won !".format(winner.mention)
            self_exp_up = await self.exp_up_vs_bot(winner)
        elif n_bot > n_author:
            # Winner
            winner = bot
            n_winner = n_bot
            dice_winner = dice_bot
            # Loser
            loser = author
            n_loser = n_author
            dice_loser = dice_author
            # End
            msg = "{} won !".format(winner.mention)
            self_exp_up = "nlvlup"
        # Tie
        else:
            winner = author
            n_winner = n_author
            dice_winner = dice_author
            loser = bot
            n_loser = n_bot
            dice_loser = dice_bot
            msg = "{} & {} : Tie ! No one wins, no one loses.".format(author.mention, bot.mention)
            self_exp_up = "nlvlup"
        # Viewing
        data = discord.Embed(description="iDice Duel <:normal_dice:380852681364865034> :crossed_swords:",
                             color=author.color)
        data.add_field(name=winner.display_name, value="{} {} {}".format(dice_winner, n_winner, dice_winner))
        data.add_field(name=loser.display_name, value="{} {} {}".format(dice_loser, n_loser, dice_loser))
        await ctx.message.delete()
        await ctx.send(embed=data, content=msg)
        # Check if leveled up
        if self_exp_up == "ylvlup":
            lvl_winner = await self.config.member(winner).lvl()
            await ctx.send("{} has leveled up to {} ! Congrats !!!".format(winner.mention, lvl_winner))


    @idice.command(name="stats")
    @commands.guild_only()
    async def idice_stats(self, ctx, type = "graph", user: discord.Member = None, lim_axis: int = 0):
        author = ctx.author
        lvl_asked = lim_axis # Using lim_axis as lvl_asked for type: bar
                             # This command first use is for type: graph
                             # but some asked for bar
        img = BytesIO()
        if user == None:
            user = author
        perso_lvl = await self.config.member(user).lvl()
        perso_exp = await self.config.member(user).exp()
        # Calculating the sum of user exp for lim_axis or bar
        x2 = [perso_lvl + perso_exp/(perso_lvl*10)]

        for i in range(1,perso_lvl+1):
            perso_exp += i*10
        if type == "graph":
            y2 = [perso_exp]
        # Exp Needed
        exp = 0
        lvl = 0
        if type == "graph":
            to_do = 100
            x = [0]
            y = [0]
        else:
            to_do = lvl_asked

        for lvl in range(0, to_do):
            exp += lvl*10
            if type == "graph":
                x.append(lvl)
                y.append(exp)

        if type == "graph":
            #  Exp axis limit for type: graph
            def y_lim_min(perso_lvl):
                exp_lim_min = 0
                if perso_lvl-lim_ask < 0:
                    return exp_lim_min
                else:
                    for k in range(0, perso_lvl-lim_ask):
                        exp_lim_min += k*10
                    return exp_lim_min

            def y_lim_max(perso_lvl):
                exp_lim_max = 0
                for m in range(0, perso_lvl+lim_ask):
                    exp_lim_max += m*10
                return exp_lim_max
            # Graph
            plt.plot(x,y)
            plt.plot(x2,y2,'o')
            plt.title("IDiceBattle\nExperience / Level")
            plt.ylabel("Exp")
            plt.xlabel("Lvl")
            plt.legend(["Experience needed", "You are here"])
            if lim_ask != 0:
                plt.xlim(perso_lvl-lim_ask,perso_lvl+lim_ask)
                plt.ylim(y_lim_min(perso_lvl), y_lim_max(perso_lvl))
            plt.savefig(io, dpi=300, bbox_inches='tight') # Need something to do w/ BytesIO
        else:
            plt.bar("Experience needed for the level {}".format(to_do), exp)
            plt.bar("You", perso_exp)
            plt.title("IDiceBattle")
            plt.ylabel("Experience")
            plt.savefig(io, dpi=300, bbox_inches='tight') # Need something to do w/ BytesIO
        # Viewing
        # Maybe something with a discord.Embed or just uploading the image like a retard
        await ctx.send(file=img)
