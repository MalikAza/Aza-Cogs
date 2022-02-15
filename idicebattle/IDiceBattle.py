# cog.name inspired by Hitsumo
# Idea developed by Aza' & Hitsumo
# cog coding by Aza' & RissCrew
# converted in V3 by Aza'
from redbot.core import commands, Config, bank, checks
from random import randint
from io import BytesIO
import io
import discord
import asyncio
import matplotlib.pyplot as plt
import aiohttp

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

async def crit_failure_img():
    async with aiohttp.ClientSession() as session:
      async with session.get('https://i.imgur.com/paUn18x.png') as w:
          data = await w.read()
          return data

async def failure_img():
    async with aiohttp.ClientSession() as session:
      async with session.get('https://i.imgur.com/ZlUJv2a.png') as w:
          data = await w.read()
          return data

async def normal_dice_img():
    async with aiohttp.ClientSession() as session:
      async with session.get('https://i.imgur.com/BJ3nNtA.png') as w:
          data = await w.read()
          return data

async def crit_success_img():
    async with aiohttp.ClientSession() as session:
      async with session.get('https://i.imgur.com/KRO8zMD.png') as w:
          data = await w.read()
          return data

class SetParser:
    def __init__(self, argument):
        allowed = ("+", "-")
        self.sum = int(argument)
        if argument and argument[0] in allowed:
            if self.sum < 0:
                self.operation = "withdraw"
            elif self.sum > 0:
                self.operation = "deposit"
            else:
                raise RuntimeError
            self.sum = abs(self.sum)
        elif argument.isdigit():
            self.operation = "set"
        else:
            raise RuntimeError

class IDiceBattle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2110932804290696)
        default_profile = {
            "lvl": 1,
            "exp": 0,
            "bonus": 0
        }
        default_global = {
            "config_done": False,
            "crit_failure": None,
            "failure": None,
            "normal_dice": None,
            "crit_success": None
        }
        self.config.register_user(**default_profile)
        self.config.register_global(**default_global)

    async def exp_up(self, user):
        exp = await self.config.user(user).exp()
        lvl = await self.config.user(user).lvl()
        bonus = await self.config.user(user).bonus()
        possible_futur_exp = (exp + 10)
        # exp_up + lvl_up
        if possible_futur_exp >= (10 * lvl):
            # lvl_up
            await self.config.user(user).lvl.set(lvl + 1)
            # reset exp
            await self.config.user(user).exp.set(0)
            # bonus_up
            await self.config.user(user).bonus.set(bonus + 1)
            return "ylvlup"
        # Normal exp_up
        else:
            await self.config.user(user).exp.set(exp + 10)
            return "nlvlup"

    async def exp_up_vs_bot(self, user):
        exp = await self.config.user(user).exp()
        lvl = await self.config.user(user).lvl()
        bonus = await self.config.user(user).bonus()
        possible_futur_exp = (exp + 1)
        # exp_up + lvl_up
        if possible_futur_exp >= (10 * lvl):
            # lvl_up
            await self.config.user(user).lvl.set(lvl + 1)
            # reset exp
            await self.config.user(user).exp.set(0)
            # bonus_up
            await self.config.user(user).bonus.set(bonus + 1)
            return "ylvlup"
        # Normal exp_up
        else:
            await self.config.user(user).exp.set(exp + 1)
            return "nlvlup"

    async def get_normal_dice(self):
        normal_dice_id = await self.config.normal_dice()
        try:
            normal = self.bot.get_emoji(normal_dice_id)
        except:
            normal = None
        return normal

    async def get_dice_emojis(self):
        crit_failure_id = await self.config.crit_failure()
        failure_id = await self.config.failure()
        normal_dice_id = await self.config.normal_dice()
        crit_success_id = await self.config.crit_success()
        try:
            crit_failure = self.bot.get_emoji(crit_failure_id)
            failure = self.bot.get_emoji(failure_id)
            normal = self.bot.get_emoji(normal_dice_id)
            crit_success = self.bot.get_emoji(crit_success_id)
        except:
            crit_failure = None
            failure = None
            normal = None
            crit_success = None
        return crit_failure, failure, normal, crit_success

    async def dice(self, bonus_user):
        crit_failure, failure, normal, crit_success = await self.get_dice_emojis()
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

        return dice_user, n_user

    @commands.group()
    @commands.guild_only()
    async def idiceset(self, ctx):
        """The differents configs for iDice."""

    @idiceset.command(name="emoji")
    @commands.guild_only()
    async def idiceset_emoji(self, ctx):
        """Install the essentials emojis.

        You can create them in any of your server, as long as the bot is in it, it can use them."""
        author = ctx.author
        server = ctx.guild
        # Checking if this command has already been used
        if not await self.config.config_done():
            # Checking if there is enough emojis slot in the server
            if not enough_emojis(server):
                # Not enough slot
                await ctx.send("You don't have enough places available in your server's emojis.\n"
                               "The iDice Battle need 4 places available in your server's emojis.")
            else:  # Enough slot and asking if it's ok to create
                msg = await ctx.send("It will take 4 places available in your server's emojis. Is it ok ?")
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                try:
                    def check(reaction, user):
                        return user == author and (reaction.emoji == '✅' or reaction.emoji == '❌')

                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    # Positive response
                    if reaction.emoji == '✅':
                        await ctx.send("The emojis have been created.")
                        # Creating emojis
                        await server.create_custom_emoji(name = "crit_failure", image = await crit_failure_img())
                        await server.create_custom_emoji(name = "failure", image = await failure_img())
                        await server.create_custom_emoji(name = "normal_dice", image = await normal_dice_img())
                        await server.create_custom_emoji(name = "crit_success", image = await crit_success_img())
                        await asyncio.sleep(1) # Debugging for emojis.id
                        # Setting config to True and adding emojis.id
                        await self.config.config_done.set(True)
                        for emoji in server.emojis:
                            if emoji.name == 'crit_failure':
                                await self.config.crit_failure.set(emoji.id)
                            elif emoji.name == 'failure':
                                await self.config.failure.set(emoji.id)
                            elif emoji.name == 'normal_dice':
                                await self.config.normal_dice.set(emoji.id)
                            elif emoji.name == 'crit_success':
                                await self.config.crit_success.set(emoji.id)
                    # Negative response
                    if reaction.emoji == '❌':
                        await ctx.send("Ok then...\nI'm not gonna create the emojis.")
                # No response
                except asyncio.TimeoutError:
                    await ctx.send("You didn't answer to me, I've stopped creating the emojis.")
        # Command has already been used
        else:
            await ctx.send("Have you forgotten? The emojis have already been created.")

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
            data.add_field(name="Level 🏆", value=await self.config.user(author).lvl())
            data.add_field(name="Experience ⭐", value=await self.config.user(author).exp())
            data.add_field(name="Bonus", value=await self.config.user(author).bonus(), inline=False)
            await ctx.message.delete()
            await ctx.send(embed=data)
        else:# No bot profile
            await ctx.send("I don't have any profile. Sorry not sorry but I'm the god of this game.")

    @idice.command(name="duel")
    @commands.guild_only()
    async def idice_duel(self, ctx, user: discord.Member, amount: int):
        """To start an iDice duel."""
        author = ctx.author
        normal_dice = await self.get_normal_dice()
        # No auto-duel
        if author == user:
            await ctx.reply("You can't duel yourself.")
        # No bot duel
        elif user == self.bot.user:
            await ctx.reply(f"Try to use `{ctx.prefix}idice pve` instead.")
        else:
            # Check if emojis are created
            if await self.config.config_done():
                # Check account.can_spend() | positive response
                if await bank.can_spend(author, amount) and await bank.can_spend(user, amount):
                    # Start w/ wait_for_reaction
                    msg1 = await ctx.send(f"{user.mention}, do you want to confront {author.mention} in an iDice duel, for an amount of {amount}?")
                    await msg1.add_reaction('✅')
                    await msg1.add_reaction('❌')
                    try:
                        def check(reaction, opponent):
                            return opponent == user and (reaction.emoji == '✅' or reaction.emoji == '❌')

                        reaction, opponent = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                        # Positive response
                        if reaction.emoji == '✅':
                            await ctx.message.delete()
                            author_bonus = await self.config.user(author).bonus()
                            user_bonus = await self.config.user(user).bonus()
                            dice_author, n_author = await self.dice(author_bonus)
                            dice_user, n_user = await self.dice(user_bonus)
                            # Results
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
                                msg = f"{winner.mention} won ! And wins the amount of {amount}."
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
                                msg = f"{author.mention} & {user.mention} : Tie ! No one wins, no one loses."
                                self_exp_up = "nlvlup"
                            # Viewing
                            data = discord.Embed(
                                description=f"iDice Duel {normal_dice} :crossed_swords:",
                                color=author.color)
                            data.add_field(name=winner.display_name,
                                           value=f"{dice_winner} {n_winner} {dice_winner}")
                            data.add_field(name=loser.display_name,
                                           value=f"{dice_loser} {n_loser} {dice_loser}")
                            await msg1.delete()
                            await ctx.send(embed=data, content=msg)
                            # Check if leveled up
                            if self_exp_up == "ylvlup":
                                lvl_winner = await self.config.user(winner).lvl()
                                await ctx.send(f"{winner.mention} has leveled up to {lvl_winner} ! Congrats !!!")
                        # Negative response
                        if reaction.emoji == '❌':
                            await msg1.delete()
                            await ctx.reply("Your opponent have no balls to confront you.")
                    # No response
                    except asyncio.TimeoutError:
                        await msg1.delete()
                        await ctx.reply("Your opponent didn't reply.")
                # author can't spend
                elif not await bank.can_spend(author, amount):
                    return await ctx.reply("You don't have enough in your bank account.\n"
                                          "Unable to proceed to an iDice duel.")
                # user can't spend
                elif not await bank.can_spend(user, amount):
                    return await ctx.reply("Your opponent don't have enough in his/her bank account.\n"
                                          "Unable to proceed to an iDice duel.")
            else:
                await ctx.reply(f"You haven't created the emojis yet, do `{ctx.prefix}idiceset emoji` for that.")

    @idice.command(name="pve")
    @commands.guild_only()
    async def idice_pve(self, ctx):
        """To start an iDice duel VS the bot."""
        author = ctx.author
        bot = self.bot.user
        author_bonus = await self.config.user(author).bonus()
        normal_dice = await self.get_normal_dice()

        # Check if emojis are created
        if await self.config.config_done():
            # Start
            dice_author, n_author = await self.dice(author_bonus)
            dice_bot, n_bot = await self.dice(int(1.5 * author_bonus))
            # Results
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
                msg = f"{winner.mention} won !"
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
                msg = f"{winner.mention} won !"
                self_exp_up = "nlvlup"
            # Tie
            else:
                winner = author
                n_winner = n_author
                dice_winner = dice_author
                loser = bot
                n_loser = n_bot
                dice_loser = dice_bot
                msg = f"{author.mention} & {bot.mention} : Tie ! No one wins, no one loses."
                self_exp_up = "nlvlup"
            # Viewing
            data = discord.Embed(description=f"iDice Duel {normal_dice} :crossed_swords:",
                                 color=author.color)
            data.add_field(name=winner.display_name, value=f"{dice_winner} {n_winner} {dice_winner}")
            data.add_field(name=loser.display_name, value=f"{dice_loser} {n_loser} {dice_loser}")
            await ctx.message.delete()
            await ctx.send(embed=data, content=msg)
            # Check if leveled up
            if self_exp_up == "ylvlup":
                lvl_winner = await self.config.user(winner).lvl()
                await ctx.send(f"{winner.mention} has leveled up to {lvl_winner} ! Congrats !!!")
        else:
            await ctx.reply(f"You haven't created the emojis yet, do `{ctx.prefix}idiceset emoji` for that.")

    @idice.command(name="stats")
    @commands.guild_only()
    async def idice_stats(self, ctx, type = "graph", user: discord.Member = None, lim_axis: int = 0):
        """To have a curve or bar graph based on your stats (Level and Experience).

        Usage: `[p]idice stats <graph_or_bar> <user> <level>`
        The `level` arguement is to see the stats around this level (for bar) or around (level - you_level - level) for graph.
        """
        author = ctx.author
        lvl_asked = lim_axis # Using lim_axis as lvl_asked for type: bar
                             # This command first use is for type: graph
                             # but some asked for bar
        img = BytesIO()
        if user == None:
            user = author
        perso_lvl = await self.config.user(user).lvl()
        perso_exp = await self.config.user(user).exp()
        # Calculating the sum of user exp for lim_axis or bar
        x2 = [perso_lvl + perso_exp / (perso_lvl * 10)]

        for i in range(1, perso_lvl + 1):
            perso_exp += i * 10
        if type == "graph":
            y2 = [perso_exp]
        # Exp Needed
        exp = 0
        lvl = 0
        to_do = 100
        if type == "graph":
            x = [0]
            y = [0]
        else:
            to_do = lvl_asked
            if to_do == 0:
                to_do = 100

        for lvl in range(0, to_do):
            exp += lvl * 10
            if type == "graph":
                x.append(lvl)
                y.append(exp)

        if type == "graph":
            #  Exp axis limit for type: graph
            def y_lim_min():
                exp_lim_min = 0
                if perso_lvl - lim_axis < 0:
                    return exp_lim_min
                elif perso_lvl - lim_axis > 100:
                    return exp_lim_min
                elif lim_axis == 0:
                    return exp_lim_min
                else:
                    for k in range(0, perso_lvl - lim_axis):
                        exp_lim_min += k * 10
                    return exp_lim_min

            def y_lim_max():
                exp_lim_max = 0
                if perso_lvl + lim_axis < 0:
                    for m in range(0, 100):
                        exp_lim_max += m * 10
                    return exp_lim_max
                elif perso_lvl + lim_axis > 100:
                    for m in range(0, 100):
                        exp_lim_max += m * 10
                    return exp_lim_max
                elif lim_axis == 0:
                    for m in range(0, 100):
                        exp_lim_max += m * 10
                    return exp_lim_max
                else:
                    for m in range(0, perso_lvl + lim_axis):
                        exp_lim_max += m * 10
                    return exp_lim_max

            def x_lim_min():
                if perso_lvl - lim_axis < 0:
                    return perso_lvl - perso_lvl
                elif perso_lvl - lim_axis > 100:
                    return perso_lvl - perso_lvl
                elif lim_axis == 0:
                    return 0
                else:
                    return perso_lvl - lim_axis

            def x_lim_max():
                if perso_lvl + lim_axis > 100:
                    return 100
                elif perso_lvl + lim_axis < 0:
                    return 100
                elif lim_axis == 0:
                    return 100
                else:
                    return perso_lvl + lim_axis
            # Graph
            plt.plot(x,y)
            plt.plot(x2,y2,'o')
            plt.title(f"{user.name} IDice Stats\nExperience / Level")
            plt.xlabel("Level")
            plt.legend(["Experience needed", "You are here"], bbox_to_anchor=(1.05, 1), loc='best', borderaxespad=0.)
            plt.xlim(x_lim_min(), x_lim_max())
            plt.ylim(y_lim_min(), y_lim_max())
        else:
            plt.bar(f"Experience\nneeded for the level {to_do}", exp)
            plt.bar("You", perso_exp)
            plt.title(f"{user.name} IDice Stats")
        plt.ylabel("Experience")
        plt.savefig(img, dpi=300, bbox_inches='tight', format="png")
        plt.close()
        # Viewing
        file_name = f"{user.name} IDice Stats - {type}.png"
        img.seek(0)
        await ctx.reply(file=discord.File(img, filename=file_name))

    @idice.command(name="setlvl")
    @commands.guild_only()
    @checks.is_owner()
    async def idice_setlvl(self, ctx, user: discord.Member, lvls: SetParser):
        """Set a user level.

        Passing positive and negative values will add/remove levels instead.

        Examples:
        - `[p]idice_setlvl @Aza' 29` - Sets levels to 29
        - `[p]idice_setlvl @Aza' +2` - Increases levels by 2
        - `[p]idice_setlvl @Aza' -9` - Decreases levels by 9
        """
        author = ctx.author
        user_lvl = await self.config.user(user).lvl()
        user_bonus = await self.config.user(user).bonus()
        # Adding level
        if lvls.operation == "deposit":
            await self.config.user(user).lvl.set(user_lvl + lvls.sum)
            await self.config.user(user).exp.set(0)
            await self.config.user(user).bonus.set(user_bonus + lvls.sum)
            msg = f"`{author.display_name}` added **{lvls.sum}** level(s) to `{user.display_name}`."
        # Removing level
        elif lvls.operation == "withdraw":
            if (user_lvl - lvls.sum) < 1:
                msg = "An user's level can't be below 1."
            else:
                await self.config.user(user).lvl.set(user_lvl - lvls.sum)
                await self.config.user(user).exp.set(0)
                await self.config.user(user).bonus.set(user_bonus - lvls.sum)
                msg = f"`{author.display_name}` removed **{lvls.sum}** level(s) to `{user.display_name}`."
        # Setting level
        elif lvls.operation == "set":
            if lvls.sum == 0:
                msg = "An user's level can't be below 1."
            else:
                await self.config.user(user).lvl.set(lvls.sum)
                await self.config.user(user).exp.set(0)
                await self.config.user(user).bonus.set(lvls.sum - 1)
                msg = f"`{author.display_name}` set `{user.display_name}`'s level(s) to **{lvls.sum}**."
        await ctx.send(msg)
