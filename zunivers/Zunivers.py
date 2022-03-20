import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from datetime import datetime
import aiohttp
# lib
from .lib.dtimestamp import DateTo
from .lib.zu_api import ZUniversProfile

def enough_emojis(server):
    nbr_emoji = 0
    for emoji in server.emojis:
        if not emoji.animated:
            nbr_emoji += 1
    if nbr_emoji <= 45:
        return True
    else:
        return False

async def zu_logo_img():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/E1FG4Nq.png') as w:
            data =  w.read()
            return data

async def poudre_icon_img():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/5rsV5fP.png') as w:
            data =  w.read()
            return data

async def monnaie_icon_img():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/kggt8lh.png') as w:
            data =  w.read()
            return data

async def cristal_icon_img():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/o4wM9l9.png') as w:
            data =  w.read()
            return data

async def rayou4_img():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/GL5c2iT.png') as w:
            data =  w.read()
            return data

class Zunivers(commands.Cog):
    """Les commandes pour Zunivers."""

    def __init__(self, bot):
        self.bot = bot
        self.gold_emoji = "\N{LARGE YELLOW CIRCLE}"
        self.config = Config.get_conf(self, identifier=20834279610181129)
        default_global = {
            "config_done": False,
            "zu_logo": None,
            "poudre_icon": None,
            "monnaie_icon": None,
            "cristal_icon": None,
            "rayou4": None
        }
        self.config.register_global(**default_global)

    def activity_emoji(self, activity):
        if activity:
            active_emoji = "\N{LARGE GREEN CIRCLE}"
        else:
            active_emoji = "\N{MEDIUM WHITE CIRCLE}"

        return active_emoji

    async def get_zu_emojis(self):
        zu_logo_id = await self.config.zu_logo()
        poudre_id = await self.config.poudre_icon()
        monnaie_id = await self.config.monnaie_icon()
        cristal_id = await self.config.cristal_icon()
        rayou4_id = await self.config.rayou4()
        try:
            zu_logo = self.bot.get_emoji(zu_logo_id)
            poudre = self.bot.get_emoji(poudre_id)
            monnaie = self.bot.get_emoji(monnaie_id)
            cristal = self.bot.get_emoji(cristal_id)
            rayou4 = self.bot.get_emoji(rayou4_id)
        except:
            zu_logo = None
            poudre = None
            monnaie = None
            cristal = None
            rayou4 = None

        return zu_logo, poudre, monnaie, cristal, rayou4


    async def profile_base(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description=f"{profile.user.rank}{profile.tradeless}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(text=f"#{profile.user.position} : {profile.user.score} points", icon_url=zu_logo)
        data.add_field(name=monnaie, value=profile.user.monnaie)
        data.add_field(name=poudre, value=profile.user.poussiere)
        data.add_field(name=cristal, value=profile.user.cristal)
        data.add_field(name="Cartes uniques", value=profile.unique_cards)
        data.add_field(name=f"{self.gold_emoji} Cartes dorées uniques", value=profile.unique_gold_cards)
        data.add_field(name="Cartes", value=profile.cards_nbrs)
        data.add_field(name="Lucky Rayou grattés", value=profile.lr_nbrs)
        data.add_field(name="Succès", value=profile.achievements)
        data.add_field(name=f"{rayou4} Pity", value=profile.pity_in)

        return data

    async def defis_one(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description=f"Défis Hebdomadaire 1 - {profile.challenge.first.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.first.progress, inline=True)
        data.add_field(name="Récompenses", value=f"{profile.challenge.first.score} points et {profile.challenge.first.poussiere} {poudre}", inline=False)

        return data

    async def defis_two(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description=f"Défis Hebdomadaire 2 - {profile.challenge.second.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.second.progress, inline=True)
        data.add_field(name="Récompenses", value=f"{profile.challenge.second.score} points et {profile.challenge.second.poussiere} {poudre}", inline=False)

        return data

    async def defis_three(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description=f"Défis Hebdomadaire 3 - {profile.challenge.third.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.third.progress, inline=True)
        data.add_field(name="Récompenses", value=f"{profile.challenge.third.score} points et {profile.challenge.first.poussiere} {poudre}", inline=False)

        return data

    async def defis_embed(self, user, avat_url, profile):
        page_one = self.defis_one(user, avat_url, profile)
        page_two = self.defis_two(user, avat_url, profile)
        page_three = self.defis_three(user, avat_url, profile)
        pages = [page_one, page_two, page_three]

        return pages

    async def sub(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description="Abonnement", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Début", value=f"{profile.subscription_begin}\nsoit {profile.subscription_begin_since}.")
        data.add_field(name="Fin", value=f"{profile.subscription_end}\nsoit {profile.subscription_end_to}.")

        return data

    async def vortex(self, user, avat_url, profile):
        active_emoji = self.activity_emoji(profile.user.actif)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        data = discord.Embed(description=f"Vortex - {profile.vortex_name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.player_url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Début", value=profile.vortex_begin_date)
        data.add_field(name="Fin", value=profile.vortex_end_date)
        data.add_field(name="Étage", value=profile.vortex_stade, inline=False)
        data.add_field(name="Essais", value=profile.vortex_trys, inline=False)

        return data

    async def profile_embed(self, user, avat_url, profile):
        pages = []
        pages.append(await self.profile_base(user, avat_url, profile))
        pages.append(await self.sub(user, avat_url, profile))
        pages.append(await self.vortex(user, avat_url, profile))
        defis = await self.defis_embed(user, avat_url, profile)
        for i in defis:
            pages.append(i)

        return pages

    @commands.group()
    @commands.guild_only()
    async def zuset(self, ctx):
        """Les différentes configurations pour Zunivers."""

    @zuset.command(name="emoji")
    @commands.guild_only()
    async def zuset_emoji(self, ctx):
        """Installe les emojis essentiels.

        Vous pouvez les créer dans n'importe lequel de vos serveurs, tant que le bot est dedans et peu les utiliser."""
        author = ctx.author
        server = ctx.guild
        # Checking if this command has already been used
        if not await self.config.config_done():
            # Checking if there is enough emojis slot in the server
            if not enough_emojis(server):
                # Not enough slot
                await ctx.send("Tu n'as pas assez d'espace d'emoji disponible dans ton serveur.\n"
                               "Zunivers a besoin de 5 places d'emojis disponibles.")
            else:  # Enough slot and asking if it's ok to create
                msg = await ctx.send("Cela prendra 5 espaces d'emoji dans ton serveur, c'est bon pour toi ?")
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                try:
                    def check(reaction, user):
                        return user == author and (reaction.emoji == '✅' or reaction.emoji == '❌')

                    reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                    # Positive response
                    if reaction.emoji == '✅':
                        await ctx.send("Les emojis ont été créés.")
                        # Creating emojis
                        await server.create_custom_emoji(name = "zu_logo", image = await zu_logo_img())
                        await server.create_custom_emoji(name = "Poudrecreatrice", image = poudre_icon_img())
                        await server.create_custom_emoji(name = "ZUMonnaie", image = await monnaie_icon_img())
                        await server.create_custom_emoji(name = "Cristaldhistoire", image = await cristal_icon_img())
                        await server.create_custom_emoji(name = "Rayou4", image = await rayou4_img())
                        await asyncio.sleep(1) # Debugging for emojis.id
                        # Setting config to True and adding emojis.id
                        await self.config.config_done.set(True)
                        for emoji in server.emojis:
                            if emoji.name == 'zu_logo':
                                await self.config.zu_logo.set(emoji.id)
                            elif emoji.name == 'Poudrecreatrice':
                                await self.config.poudre_icon.set(emoji.id)
                            elif emoji.name == 'ZUMonnaie':
                                await self.config.monnaie_icon.set(emoji.id)
                            elif emoji.name == 'Cristaldhistoire':
                                await self.config.cristal_icon.set(emoji.id)
                            elif emoji.name == 'Rayou4':
                                await self.config.rayou4.set(emoji.id)
                    # Negative response
                    if reaction.emoji == '❌':
                        await ctx.send("Bon d'accords...\nJe ne vais pas créer les emojis.")
                # No response
                except asyncio.TimeoutError:
                    await ctx.send("Tu ne m'as pas répondu, j'ai stoppé la création des emojis.")
        # Command has already been used
        else:
            await ctx.send("Tu as oublié ? TLes emojis ont déjà été créés.")

    @commands.group()
    async def zu(self, ctx):
        """Commandes de bases pour ZUnivers."""

    @zu.command(name="profile")
    async def zu_profile(self, ctx, user : discord.User = None):
        """Profil de l'utilisateur contenant toutes les informations."""
        if await self.config.config_done():
            author = ctx.author
            if user == None:
                user = author

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            username = user.name
            discri = user.discriminator

            profile = ZUniversProfile(username, discri)
            data = await self.profile_embed(user, avat_url, profile)

            await menu(ctx, data, DEFAULT_CONTROLS)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")
        
    @zu.command(name="defis")
    async def zu_defis(self, ctx, user : discord.User = None):
        """Défis et leurs progressions de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            if user == None:
                user = author

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            username = user.name
            discri = user.discriminator

            profile = ZUniversProfile(username, discri)
            data = await self.defis_embed(user, avat_url, profile)

            await menu(ctx, data, DEFAULT_CONTROLS)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    @zu.command(name="subscription", aliases=['sub'])
    async def zu_subscription(self, ctx, user : discord.User = None):
        """Abonnement de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            if user == None:
                user = author

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            username = user.name
            discri = user.discriminator

            profile = ZUniversProfile(username, discri)
            data = await self.sub(user, avat_url, profile)

            await ctx.send(embed=data)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    @zu.command(name="vortex", aliases=['as'])
    async def zu_vortex(self, ctx, user : discord.User = None):
        """Vortex de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            if user == None:
                user = author

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            username = user.name
            discri = user.discriminator

            profile = ZUniversProfile(username, discri)
            data = await self.vortex(user, avat_url, profile)

            await ctx.send(embed=data)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")