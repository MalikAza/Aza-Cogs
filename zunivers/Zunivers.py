import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from datetime import datetime
import aiohttp
# lib
from .lib.dtimestamp import DateTo
from .lib.zu_api import *

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
        active_emoji = self.activity_emoji(profile.active)
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        if profile.journa:
            journa_emoji = "✅"
        else:
            journa_emoji = "❌"
        if profile.tradeless:
            profile.tradeless = ", Sans échange"
        else:
            profile.tradeless = ""
        data = discord.Embed(description=f"{profile.rank}{profile.tradeless}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(text=f"#{profile.position} : {profile.score} points", icon_url=zu_logo)
        data.add_field(name=monnaie, value=profile.monnaie)
        data.add_field(name=poudre, value=profile.powder)
        data.add_field(name=cristal, value=profile.crystal)
        data.add_field(name="Cartes uniques", value=profile.unique_cards)
        data.add_field(name=f"{self.gold_emoji} Cartes dorées uniques", value=profile.unique_gold_cards)
        data.add_field(name="Cartes", value=profile.card_numbers)
        data.add_field(name="Lucky Rayou grattés", value=profile.lucky_numbers)
        data.add_field(name="Succès", value=profile.achievement_numbers)
        data.add_field(name=f"{rayou4} Pity", value=profile.pity_in)
        data.add_field(name="!journa", value=journa_emoji)

        return data

    async def defis_one(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        data = discord.Embed(description=f"Défis Hebdomadaire 1 - {profile.challenge.first.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.first.progress, inline=True)
        data.add_field(name="Récompenses",
        value=f"{profile.challenge.first.score_gain} points et {profile.challenge.first.powder_gain} {poudre}", inline=False)

        return data

    async def defis_two(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        data = discord.Embed(description=f"Défis Hebdomadaire 2 - {profile.challenge.second.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.second.progress, inline=True)
        data.add_field(name="Récompenses",
        value=f"{profile.challenge.second.score_gain} points et {profile.challenge.second.powder_gain} {poudre}", inline=False)

        return data

    async def defis_three(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        data = discord.Embed(description=f"Défis Hebdomadaire 3 - {profile.challenge.third.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Progression", value=profile.challenge.third.progress, inline=True)
        data.add_field(name="Récompenses",
        value=f"{profile.challenge.third.score_gain} points et {profile.challenge.first.powder_gain} {poudre}", inline=False)

        return data

    async def defis_embed(self, user, avat_url, profile):
        page_one = await self.defis_one(user, avat_url, profile)
        page_two = await self.defis_two(user, avat_url, profile)
        page_three = await self.defis_three(user, avat_url, profile)
        pages = [page_one, page_two, page_three]

        return pages

    async def sub(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        data = discord.Embed(description="Abonnement", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        if profile.is_subscribed:
            data.add_field(name="Début", value=f"{profile.subscription_begin}\nsoit {profile.subscription_begin_since}.")
            data.add_field(name="Fin", value=f"{profile.subscription_end}\nsoit {profile.subscription_end_to}.")
        else:
            data.add_field(name="Aucun abonnement", value="🚫")

        return data

    async def vortex(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        vortex = Vortex()
        data = discord.Embed(description=f"Vortex - {vortex.name}", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        data.add_field(name="Début", value=vortex.begin_date)
        data.add_field(name="Fin", value=vortex.end_date)
        data.add_field(name="Étage", value=profile.vortex_stade, inline=False)
        data.add_field(name="Essais", value=profile.vortex_trys, inline=False)

        return data

    async def reputation(self, user, avat_url, profile):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        active_emoji = self.activity_emoji(profile.active)
        data = discord.Embed(description="Réputations", color=user.color)
        data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
        data.set_footer(icon_url=zu_logo)
        # one
        data.add_field(name=profile.reputation.first.name,
        value=f"*{profile.reputation.first.level_name}*\n{profile.reputation.first.progress}")
        # two
        data.add_field(name=profile.reputation.second.name,
        value=f"*{profile.reputation.second.level_name}*\n{profile.reputation.second.progress}")
        # three
        data.add_field(name=profile.reputation.third.name,
        value=f"*{profile.reputation.third.level_name}*\n{profile.reputation.third.progress}")
        # four
        data.add_field(name=profile.reputation.fourth.name,
        value=f"*{profile.reputation.fourth.level_name}*\n{profile.reputation.fourth.progress}")
        # five
        data.add_field(name=profile.reputation.fifth.name,
        value=f"*{profile.reputation.fifth.level_name}*\n{profile.reputation.fifth.progress}")

        return data

    async def events(self, datas):
        zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()
        pages = []
        for i in range(len(datas.names)):
            emb = discord.Embed(title="Evènement(s) en cours...", description=datas.names[i], color=discord.Colour(value=0x19BC14))
            emb.set_footer(icon_url=zu_logo)
            emb.add_field(name="Début", value=datas.begin_dates[i])
            emb.add_field(name="Fin", value=datas.end_dates[i])
            emb.add_field(name="Pack", value=datas.pack_names[i])
            if datas.is_onetimes[i]:
                one_time = "Oui"
            else:
                one_time = "Non"
            emb.add_field(name="Une seule fois", value=one_time)
            if datas.actives[i]:
                active = "Oui"
            else:
                active = "Non"
            emb.add_field(name="Actuellement actif", value=active)
            emb.add_field(name=monnaie, value=datas.monney_costs[i])
            emb.add_field(name=poudre, value=datas.dust_costs[i])
            pages.append(emb)

        return pages

    async def profile_embed(self, user, avat_url, profile):
        pages = []
        pages.append( await self.profile_base(user, avat_url, profile))
        pages.append( await self.sub(user, avat_url, profile))
        pages.append( await self.vortex(user, avat_url, profile))
        pages.append( await self.reputation(user, avat_url, profile))
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

    @zu.command(name="profile", aliases=["profil"])
    async def zu_profile(self, ctx, user : discord.User = None):
        """Profil de l'utilisateur contenant toutes les informations."""
        if await self.config.config_done():
            author = ctx.author
            server = ctx.guild
            if user == None:
                user = author
            else:
                try:
                    user = await server.fetch_member(user.id)
                except:
                    pass

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            profile = User(user)
            data = await self.profile_embed(user, avat_url, profile)

            await menu(ctx, data, DEFAULT_CONTROLS)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")
        
    @zu.command(name="defis")
    async def zu_defis(self, ctx, user : discord.User = None):
        """Défis et leurs progressions de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            server = ctx.guild
            if user == None:
                user = author
            else:
                try:
                    user = await server.fetch_member(user.id)
                except:
                    pass

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            profile = User(user)
            data = await self.defis_embed(user, avat_url, profile)

            await menu(ctx, data, DEFAULT_CONTROLS)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    @zu.command(name="subscription", aliases=['sub'])
    async def zu_subscription(self, ctx, user : discord.User = None):
        """Abonnement de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            server = ctx.guild
            if user == None:
                user = author
            else:
                try:
                    user = await server.fetch_member(user.id)
                except:
                    pass

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            profile = User(user)
            data = await self.sub(user, avat_url, profile)

            await ctx.send(embed=data)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    @zu.command(name="vortex", aliases=['as'])
    async def zu_vortex(self, ctx, user : discord.User = None):
        """Vortex de l'utilisateur."""
        if await self.config.config_done():
            author = ctx.author
            server = ctx.guild
            if user == None:
                user = author
            else:
                try:
                    user = await server.fetch_member(user.id)
                except:
                    pass

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            profile = User(user)
            data = await self.vortex(user, avat_url, profile)

            await ctx.send(embed=data)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    # zu_insomniaque
    @zu.command(name="insomniaque", aliases=['dodopa'])
    async def zu_insomniaque(self, ctx, user : discord.User = None):
        """Affiche le statut de l'utilisateur pour l'achievement 'Insomniaque'."""
        if await self.config.config_done():
            author = ctx.author
            server = ctx.guild
            if user == None:
                user = author
            else:
                try:
                    user = await server.fetch_member(user.id)
                except:
                    pass

            if user.is_avatar_animated():
                avat_url = str(user.avatar_url_as(format="gif"))
            else:
                avat_url = str(user.avatar_url_as(static_format="png"))

            profile = User(user)
            insomniaque = Insomniaque(user)

            active_emoji = self.activity_emoji(profile.active)
            zu_logo, poudre, monnaie, cristal, rayou4 = await self.get_zu_emojis()

            data = discord.Embed(description=f"Achievement - {insomniaque.name}", color=user.color)
            data.set_author(name=f"{user} {active_emoji}", icon_url=avat_url, url=profile.url)
            data.set_footer(icon_url=zu_logo)
            if not insomniaque.done:
                done = insomniaque.progress_done
                todo = insomniaque.progress_todo
                def str_insomn(lis):
                    if len(lis) == 1:
                        return lis[0]
                    else:
                        return ", ".join([str(x)  if i%int(len(lis)/2) !=0 else f"\n{x}" for i,x in enumerate(lis)])

                data.add_field(name="✅ Fait(s)", value=str_insomn(done), inline=True)
                data.add_field(name="❌ À faire(s)",value=str_insomn(todo), inline=True)
            else:
                data.add_field(name="GG à toi !", value="Tu as déjà accomplis cet achievement.", inline=True)

            await ctx.send(embed=data)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")

    # zu_event
    @zu.command(name="event")
    async def zu_event(self, ctx):
        """Affiche les événements en cours."""

        if await self.config.config_done():
            event_datas = Event()
            if not event_datas.got_events:
                await ctx.reply("Aucun événement en cours.")
            else:
                embeds = await self.events(event_datas)
                await menu(ctx, embeds, DEFAULT_CONTROLS)
        else:
            await ctx.reply(f"Tu n'as pas encore créé les emojis, tappe `{ctx.prefix}zuset emoji` pour cela.")