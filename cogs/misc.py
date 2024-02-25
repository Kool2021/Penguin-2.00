import asyncio
import random
import time
from datetime import datetime

import aiohttp
import discord
import requests
from discord import Game, Spotify
from discord.ext import commands
import humanize

snipe_message_author = {}
snipe_message_content = {}
esnipe_message_author = {}
esnipe_message_content_before = {}
esnipe_message_content_after = {}


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


class Misc(commands.Cog):
    """Miscellaneous commands ig?"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def snipe(self, ctx):
        """Snipes deleted messages, shows up to 5"""
        channel = ctx.channel
        try:
            em = discord.Embed(
                title=f"Last deleted message in {channel.name}",
                description=f"```{snipe_message_content[channel.id][0]}``` \n",
                color=0x006BB6,
            )
            em.set_footer(text=f"The latest deleted message was sent by {snipe_message_author[channel.id][0]}")
            if len(snipe_message_author[channel.id]) > 1:
                value = ""
                for x in range(len(snipe_message_author[channel.id]) - 1):
                    if x == 5:
                        break
                    value += f"{x+1}. `{snipe_message_content[channel.id][x + 1]}`: {snipe_message_author[channel.id][x + 1]} \n"
                em.add_field(name="Earlier Deleted Messages", value=f"{value}", inline=False)
            await ctx.send(embed=em)
        except:
            await ctx.send(f"There are no recently deleted messages in {channel.mention}")

    @commands.command(aliases=["editsnipe"])
    async def esnipe(self, ctx):
        """Snipe, but for edits"""
        channel = ctx.channel
        try:
            em = discord.Embed(
                title=f"Last edited message in {channel.name}", description="Caught red-handed :D", color=0x006BB6
            )
            em.add_field(name="Before", value=f"```{esnipe_message_content_before[channel.id][0]}```", inline=False)
            em.add_field(name="After", value=f"```{esnipe_message_content_after[channel.id][0]}```")
            if len(esnipe_message_author[channel.id]) > 1:
                value = ""
                for x in range(len(esnipe_message_author[channel.id]) - 1):
                    if x == 5:
                        break
                    value += f"{x+1}. `{esnipe_message_content_before[channel.id][x + 1]}` -> `{esnipe_message_content_after[channel.id][x + 1]}`:  {esnipe_message_author[channel.id][x + 1]}\n"
                em.add_field(name="Even Earlier Edits", value=f"{value}", inline=False)
            em.set_footer(text=f"The latest message was sent and edited by {esnipe_message_author[channel.id][0]}")
            await ctx.send(embed=em)
        except:
            await ctx.send(f"There are no recently edited messages in #{channel.name}")

    @commands.command()
    async def swagles(self, ctx):
        """I forget why I made this"""
        await ctx.send(random.choice(["Les is swag af", "Les is swagger that the swaggest of the swag", "Les is swag"]))

    @commands.command()
    async def jellyfish(self, ctx):
        """Wanna see a jellyfish GIF?"""
        em = discord.Embed(title=f"JELLYFISH", description="Jellyfishes are awesome.")
        url = random.choice(
            [
                "https://media.giphy.com/media/2dwejHC0H3mta/giphy.gif",
                "https://media.giphy.com/media/LPlmexh8SLjO9OwPxP/giphy.gif",
                "https://media.giphy.com/media/xTeV7AzV5rhNBO1r1u/giphy.gif",
                "https://media.giphy.com/media/3ohzAjPbJz1UiQPYha/giphy.gif",
            ]
        )
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command()
    async def fail(self, ctx):
        """Epic fails that will make you laugh"""
        em = discord.Embed(title="EPIC FAIL", description="This makes me laugh-")
        url = random.choice(
            [
                "https://media.giphy.com/media/BvBEozfsXWWHe/giphy.gif",
                "https://media.giphy.com/media/l3vRcQzQARIkhawYU/giphy.gif",
                "https://media.giphy.com/media/jiiRUIaVpG89i/giphy.gif",
                "https://media.giphy.com/media/TpkhbFd6ap0pq/giphy.gif",
            ]
        )
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command()
    async def warriors(self, ctx):
        """Displays the Golden State Warriors logo"""
        em = discord.Embed(title="Warriors Logo", description="2022 Champs", color=0x1D428A)
        em.set_image(
            url="https://upload.wikimedia.org/wikipedia/en/thumb/0/01/Golden_State_Warriors_logo.svg/1200px-Golden_State_Warriors_logo.svg.png"
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["mvp", "curry"])
    async def steph(self, ctx):
        """Steph Curry GIF!"""
        em = discord.Embed(title="Chef Curry", description="2022 MVP", color=0x1D428A)
        em.set_image(url="https://media.giphy.com/media/1WYkuncFSJJi1v8eWR/giphy.gif")
        await ctx.send(embed=em)

    @commands.command()
    async def klay(self, ctx):
        """Klay Thompson GIF!"""
        em = discord.Embed(title="Game 6 Klay", description="2022 Three Point Contest Champ", color=0x1D428A)
        em.set_image(url="https://media.giphy.com/media/3oriNMgvxbg1O6iq3e/giphy.gif")
        await ctx.send(embed=em)

    @commands.command()
    async def oubre(self, ctx):
        """Kelly Oubre Jr. GIF!"""
        em = discord.Embed(title="Tsunami Papi", description="Future All-Star", color=0x1D428A)
        em.set_image(
            url="https://images-ext-1.discordapp.net/external/aavLxoajb7Ox3PExLDki21IISlyR3Oevp0dYomkMe_Y/https/media.discordapp.net/attachments/797250683430633517/824391158494920785/pogopgpgopgo.gif"
        )
        await ctx.send(embed=em)

    @commands.command()
    async def poole(self, ctx):
        """Jordan Poole GIF!"""
        em = discord.Embed(title="Next Air Jordan", description="POOLE PARTY!", color=0x1D428A)
        em.set_image(
            url="https://media.discordapp.net/attachments/797250683430633517/829812247924178975/lmfa_poole.gif"
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["dray"])
    async def draymond(self, ctx):
        """Draymond Green GIF!"""
        em = discord.Embed(title="Drayyyyy", description="2022 DPOY and Assists Leader", color=0x1D428A)
        em.set_image(url="https://media.giphy.com/media/wODxPdYYSq31C/giphy.gif")
        await ctx.send(embed=em)

    @commands.command(name="dog", aliases=["dogimage", "doggo", "dogs"])
    async def dog_image(self, ctx):
        "Yes, Dog Image"
        colors = [0x4DEEEA, 0x74EE15, 0xFFE700, 0xF000FF]
        res = requests.get("https://dog.ceo/api/breeds/image/random").json()
        em = discord.Embed(title="Dog Pic :dog:", color=random.choice(colors))
        em.set_image(url=res["message"])
        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if len(message.attachments) > 0:
            message_content = message.attachments[0].url
        else:
            message_content = message.content
        try:
            snipe_message_author[message.channel.id]
        except:
            snipe_message_author[message.channel.id] = []
            snipe_message_content[message.channel.id] = []
        snipe_message_author[message.channel.id] = [message.author.name, *snipe_message_author[message.channel.id]]
        snipe_message_content[message.channel.id] = [message_content, *snipe_message_content[message.channel.id]]
        await asyncio.sleep(600)
        snipe_message_author[message.channel.id].pop()
        snipe_message_content[message.channel.id].pop()

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        try:
            esnipe_message_author[message_before.channel.id]
        except:
            esnipe_message_author[message_before.channel.id] = []
            esnipe_message_content_before[message_before.channel.id] = []
            esnipe_message_content_after[message_before.channel.id] = []

        esnipe_message_author[message_before.channel.id] = [
            message_before.author.name,
            *esnipe_message_author[message_before.channel.id],
        ]
        esnipe_message_content_before[message_before.channel.id] = [
            message_before.content,
            *esnipe_message_content_before[message_before.channel.id],
        ]
        esnipe_message_content_after[message_before.channel.id] = [
            message_after.content,
            *esnipe_message_content_after[message_after.channel.id],
        ]
        await asyncio.sleep(600)
        esnipe_message_author[message_before.channel.id].pop()
        esnipe_message_content_before[message_before.channel.id].pop()
        esnipe_message_content_after[message_before.channel.id].pop()

    @commands.command(aliases=["listening"])
    async def spotify(self, ctx, user: discord.Member = None):
        """Detects what a user is listening to on Spotify, if they have it connected to Discord."""
        user = user or ctx.author
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(
                        title=f"{user.name}'s Spotify",
                        description="Listening to {}".format(activity.title),
                        color=0xC902FF,
                    )
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.add_field(name="Duration", value=activity.duration, inline=False)
                    start_time = activity.created_at
                    end_time = activity.end
                    start_time = datetime_from_utc_to_local(start_time)
                    end_time = datetime_from_utc_to_local(end_time)
                    embed.set_footer(
                        text="Song started at {} PST, expected to finish at {}".format(
                            start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M%:%S")
                        )
                    )
                    return await ctx.send(embed=embed)

        await ctx.send(f"**{user.name}** is not listening to anything")

    @commands.command(aliases=["gaming"])
    async def playing(self, ctx, user: discord.Member = None):
        """Gets the user's playing status"""
        user = user or ctx.author
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Game):
                    embed = discord.Embed(
                        title=f"{user.name}", description="Playing {}".format(activity.name), color=0xC902FF
                    )

                    start_time = activity.start
                    start_time = datetime_from_utc_to_local(start_time)

                    embed.set_footer(text="Started playing at {} PST".format(start_time.strftime("%H:%M")))

                    return await ctx.send(embed=embed)

        await ctx.send(f"**{user.name}** is not playing anything")

    @commands.command()
    async def lyrics(self, ctx, artist, *, title):
        """Lyric search! Warning: Extremely slow, and most likely won't work. Do **?lyrics [artist] [title]**"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.lyrics.ovh/v1/{artist}/{title}") as response:
                data = await response.json()
                lyrics = data["lyrics"]
                if lyrics is None:
                    await ctx.send("Song not found! Please enter correct Artist and Song title")
                if len(lyrics) > 2000:
                    lyrics = lyrics[:2000]
                emb = discord.Embed(title=f"{title}", description=f"{lyrics}", color=0xA3A3FF)
                await ctx.send(embed=emb)
        await session.close()

    @commands.command(name="perms", aliases=["perms_for", "permissions"])
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        """
        A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked.
        """

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = "\n".join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title="Permissions for:", description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name="\uFEFF", value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.


    @commands.command()
    async def uptime(self, ctx):
        """Uptime of the bot"""
        uptime = datetime.utcnow() - self.bot.uptime
        await ctx.send(f"I have been up for {humanize.precisedelta(uptime, format='%0.0f')}")



def setup(bot):
    bot.add_cog(Misc(bot))
