import asyncio
import json
import random
import re
import traceback

import discord
from discord.ext import commands

TIME_REGEX = re.compile(r"^((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm)))$")


def random_color():
    return random.randint(0, 0xFFFFFF)


def is_valid_time(t):
    matches = TIME_REGEX.findall(str(t))
    try:
        matches[0]
    except IndexError:
        return False
    return True


class Events(commands.Cog):
    """Check your event wins count and do much more event-related things with the commands here!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="event", aliases=["events", "evnt"])
    async def event(self, ctx):
        """This may look like a small category, but there are many subcommands. You can do **?event wins** to check your event wins in the server, and **?event lb** to check the leaderboard for wins! Event managers unlock even more subcommands!"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand. An example would be `?event lb`.")

    @event.command(
        name="addwins",
        aliases=["aw", "aws", "awins"],
    )
    @commands.has_role("⋆ Event Managers")
    async def add_wins(
        self,
        ctx,
        user: discord.Member = None,
        amount: int = 1,
    ):
        try:
            with open("database/eventwins.json", "r") as f:
                data = json.load(f)
            data[str(user.id)]["wins"] += amount
            await ctx.send("Success.")
            with open("database/eventwins.json", "w") as f:
                data = json.dump(data, f, indent=4)
        except:
            with open("database/eventwins.json", "r") as f:
                data = json.load(f)
            fmt = {"wins": 0}

            user_id = str(user.id)
            data[user_id] = fmt

            data[str(user.id)]["wins"] += amount

            with open("database/eventwins.json", "w") as f:
                data = json.dump(data, f, indent=4)

            await ctx.send("Success.")

    @event.command(name="wins", aliases=["ws", "w", "dubs"])
    async def event_wins(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        try:
            with open("database/eventwins.json", "r") as f:
                data = json.load(f)
            await ctx.send(f"{user} has {data[str(user.id)]['wins']} event wins.")
        except:
            with open("database/eventwins.json", "r") as f:
                data = json.load(f)
            fmt = {"wins": 0}

            user_id = str(user.id)
            data[user_id] = fmt

            await ctx.send(f"{user} has 0 event wins.")

            with open("database/eventwins.json", "w") as f:
                data = json.dump(data, f, indent=4)

    @event.command(
        name="leaderboard",
        aliases=["lb", "leader"],
    )
    async def event_lb(self, ctx):
        with open("database/eventwins.json", "r") as f:
            data = json.load(f)

        leader_board = {}
        total = []

        for user in data:
            name = int(user)
            total_amount = data[user]["wins"]
            if total_amount in total:
                leader_board[total_amount].append(name)
            else:
                leader_board[total_amount] = [name]
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(
            title="Top 10 Event Winners",
            description="This is decided by the amount of wins in events that each person has.",
            color=0x0000FF,
        )
        index = 1
        x = 0
        prevamt = 0
        newamt = 0
        for amt in total:
            newamt = amt
            if newamt != prevamt:
                x = 0
            id_ = leader_board[amt][x]
            try:
                member_ = ctx.guild.get_member(int(id_))
                name = member_.name
                em.add_field(
                    name=f"{index}. {name}",
                    value=f"{amt}",
                    inline=False,
                )
            except:
                index -= 1
            x += 1

            if index == 10:
                break
            else:
                index += 1
            prevamt = amt

        await ctx.send(embed=em)

    @event.command(name="create", aliases=["crt"])
    @commands.has_role("⋆ Event Managers")
    async def event_create(self, ctx):
        ctx.author
        user_id = ctx.author.id
        eventchannel = self.bot.get_channel(801917409279606844)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("What do you want to title the event?")

        try:
            res = await self.bot.wait_for(
                "message",
                check=check,
                timeout=20.0,
            )
        except asyncio.TimeoutError:
            await ctx.send("You're taking too long. Sorry. :P")
            return

        event_title = "**" + res.content + "**"

        await ctx.send("What do you want the description of the event to be?")

        try:
            res = await self.bot.wait_for(
                "message",
                check=check,
                timeout=20.0,
            )
        except asyncio.TimeoutError:
            await ctx.send("You're taking too long. Sorry. :P")
            return
        event_description = res.content

        await ctx.send("At what time do you want your event to be? Please answer in the form `5:30 PM` (Pacific Time)")

        try:
            res = await self.bot.wait_for(
                "message",
                check=check,
                timeout=20.0,
            )

        except asyncio.TimeoutError:
            await ctx.send("You're taking too long. Sorry. :P")
            return

        if bool(is_valid_time(res.content)):  # IF THE TIME IS VALID
            await ctx.send("Alrighty.")
            try:
                event_time = res.content + " Pacific Standard Time"

                eventem = discord.Embed(
                    title=event_title,
                    description=event_description,
                    color=random_color(),
                )
                eventem.add_field(name="Time", value=event_time)
                emojis = ["✅", "❌", "❓"]

                eventem.add_field(
                    name="Accepted",
                    value=">>> -",
                    inline=False,
                )
                eventem.add_field(
                    name="Declined",
                    value=">>> -",
                    inline=False,
                )
                eventem.add_field(
                    name="Tentative",
                    value=">>> -",
                    inline=False,
                )
                # now = datetime.now()

                # current_time = now.strftime('%m/%d/%Y, %H:%M:%S')
                eventem.set_footer(text=f"Hosted by {ctx.author.name}.")
                emb = await eventchannel.send(embed=eventem)
                for emoji in emojis:
                    await emb.add_reaction(emoji)
                    # user_id = str(user_id)

                fmt = {
                    "name": event_title,
                    "description": event_description,
                    "time": event_time,
                    "accepted": "-",
                    "declined": "-",
                    "tentative": "-",
                    "creator": user_id,
                    "creation time": emb.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                }

                with open("database/events.json", "r") as f:
                    info = json.load(f)
                creationtime = emb.created_at.strftime("%m/%d/%Y, %H:%M:%S")
                info[creationtime] = fmt
                with open("database/events.json", "w") as f:
                    info = json.dump(info, f, indent=4)

                await ctx.send("Success! Created the event. Check the event updates channel, it should be there.")
            except:
                traceback.print_exc()
        else:

            return await ctx.send("That is not a valid time! Aborting.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # sourcery no-metrics
        if payload.channel_id != 801917409279606844:
            return
        payload.user_id
        emoji = payload.emoji
        # reactions = emb_id.reactions
        if payload.member.bot:
            return
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        users = []
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.append(user.name)
        # print(users)
        if users.count(payload.member.name) > 1:
            return

        creationtime = msg.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        creationtime = str(creationtime)
        with open("database/events.json", "r") as f:
            info = json.load(f)
        if emoji.name == "✅":
            if "-" in info[creationtime]["accepted"]:
                info[creationtime]["accepted"] = info[creationtime]["accepted"].replace("-", payload.member.name)
            else:
                info[creationtime]["accepted"] += "\n"
                info[creationtime]["accepted"] += payload.member.name
        if emoji.name == "❌":
            if "-" in info[creationtime]["declined"]:
                info[creationtime]["declined"] = info[creationtime]["declined"].replace("-", payload.member.name)
            else:
                info[creationtime]["declined"] += "\n"
                info[creationtime]["declined"] += payload.member.name
        if emoji.name == "❓":
            if "-" in info[creationtime]["tentative"]:
                info[creationtime]["tentative"] = info[creationtime]["tentative"].replace("-", payload.member.name)
            else:
                info[creationtime]["tentative"] += "\n"
                info[creationtime]["tentative"] += payload.member.name

        with open("database/events.json", "w") as f:
            info = json.dump(info, f, indent=4)

        with open("database/events.json", "r") as f:
            info = json.load(f)
        eventem1 = discord.Embed(
            title=info[creationtime]["name"],
            description=info[creationtime]["description"],
            color=random_color(),
        )
        eventem1.add_field(
            name="Time",
            value=info[creationtime]["time"],
        )
        eventem1.add_field(
            name="Accepted",
            value=f">>> {info[creationtime]['accepted']}",
            inline=False,
        )
        eventem1.add_field(
            name="Declined",
            value=f">>> {info[creationtime]['declined']}",
            inline=False,
        )
        eventem1.add_field(
            name="Tentative",
            value=f">>> {info[creationtime]['tentative']}",
            inline=False,
        )
        host = info[creationtime]["creator"]
        host = await self.bot.fetch_user(host)
        host = host.name
        eventem1.set_footer(text=f"Hosted by {host}.")
        await msg.edit(embed=eventem1)
        with open("database/events.json", "w") as f:
            info = json.dump(info, f, indent=4)
        await asyncio.sleep(0.7)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        member = str(member.name)
        emoji = payload.emoji
        # reactions = emb_id.reactions

        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.channel_id != 801917409279606844:
            return

        creationtime = msg.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        creationtime = str(creationtime)
        with open("database/events.json", "r") as f:
            info = json.load(f)
        # print(payload.member.name)
        if emoji.name == "✅":
            if info[creationtime]["accepted"] == member:
                info[creationtime]["accepted"] = info[creationtime]["accepted"].replace(member, "-")
            elif info[creationtime]["accepted"].startswith(member):
                info[creationtime]["accepted"] = info[creationtime]["accepted"].replace(f"{member}\n", "")
            else:
                info[creationtime]["accepted"] = info[creationtime]["accepted"].replace(f"\n{member}", "")
        if emoji.name == "❌":
            if info[creationtime]["declined"] == member:
                info[creationtime]["declined"] = info[creationtime]["declined"].replace(member, "-")
            elif info[creationtime]["declined"].startswith(member):
                info[creationtime]["declined"] = info[creationtime]["declined"].replace(f"{member}\n", "")
            else:
                info[creationtime]["declined"] = info[creationtime]["declined"].replace(f"\n{member}", "")
        if emoji.name == "❓":
            if info[creationtime]["tentative"] == member:
                info[creationtime]["tentative"] = info[creationtime]["tentative"].replace(member, "-")
            elif info[creationtime]["tentative"].startswith(member):
                info[creationtime]["tentative"] = info[creationtime]["tentative"].replace(f"{member}\n", "")
            else:
                info[creationtime]["tentative"] = info[creationtime]["tentative"].replace(f"\n{member}", "")

        # info[creationtime]["accepted"] += "\n"
        with open("database/events.json", "w") as f:
            info = json.dump(info, f, indent=4)

        with open("database/events.json", "r") as f:
            info = json.load(f)
        eventem1 = discord.Embed(
            title=info[creationtime]["name"],
            description=info[creationtime]["description"],
            color=random_color(),
        )
        eventem1.add_field(
            name="Time",
            value=info[creationtime]["time"],
        )
        eventem1.add_field(
            name="Accepted",
            value=f">>> {info[creationtime]['accepted']}",
            inline=False,
        )
        eventem1.add_field(
            name="Declined",
            value=f">>> {info[creationtime]['declined']}",
            inline=False,
        )
        eventem1.add_field(
            name="Tentative",
            value=f">>> {info[creationtime]['tentative']}",
            inline=False,
        )
        host = info[creationtime]["creator"]
        host = await self.bot.fetch_user(host).name
        eventem1.set_footer(text=f"Hosted by {host}.")
        await msg.edit(embed=eventem1)
        with open("database/events.json", "w") as f:
            info = json.dump(info, f, indent=4)
        await asyncio.sleep(0.5)


def setup(bot):
    bot.add_cog(Events(bot))
