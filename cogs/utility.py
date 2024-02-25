import asyncio
import json
import math
import operator
import random
import time
import traceback
from datetime import datetime

import discord
import googletrans
import requests
import wikipedia
import wolframalpha
from discord.ext import commands
from googletrans import Translator

import espn_scoreboard

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.ipow,
}


def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a % b
    return a


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def simplify_fraction(numer, denom):

    if denom == 0:
        return "Division by 0 - result undefined"

    # Remove greatest common divisor:
    common_divisor = gcd(numer, denom)
    (reduced_num, reduced_den) = (numer / common_divisor, denom / common_divisor)
    # Note that reduced_den > 0 as documented in the gcd function.

    if reduced_den == 1:
        return "`%d/%d is simplified to %d`" % (numer, denom, reduced_num)
    elif common_divisor == 1:
        return "%d/%d is already at its most simplified state" % (numer, denom)
    else:
        return "`%d/%d is simplified to %d/%d`" % (numer, denom, reduced_num, reduced_den)


def clean_time(delta_seconds):
    if delta_seconds < 0:
        ago = True
        delta_seconds = -delta_seconds
    else:
        ago = False

    hours, remainder = divmod(int(delta_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        fmt = "{d}d {h}h {m}m {s}s"
    elif hours:
        fmt = "{h}h {m}m {s}s"
    elif minutes:
        fmt = "{m}m {s}s"
    else:
        fmt = "{s}s"

    fmt = fmt.format(d=days, h=hours, m=minutes, s=seconds)
    if ago:
        return f"{fmt} ago"
    return fmt


def decode_binary_string(s):
    if " " in s:
        s = s.replace(" ", "")
    return "".join(chr(int(s[i * 8 : i * 8 + 8], 2)) for i in range(len(s) // 8))


class Utility(commands.Cog):
    """
    Some very helpful commands that you should know about
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="todo")
    async def todo(self, ctx):
        """
        A todo list is great if you forget things. The three subcommands are **?todo list**, **?todo add**, and **todo remove**.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide an action. E.g. `?todo list`, `?todo add`, `?todo remove`")

    @todo.command(name="list", aliases=["show"])
    async def todolist(self, ctx):
        with open("database/todolist.json", "r") as f:
            data = json.load(f)
        try:
            todolist = data[str(ctx.author.id)]["todolist"]
            if todolist == []:
                em = discord.Embed(
                    title=f"{ctx.author.name}'s To-Do List",
                    description="This user has nothing on their to-do list.",
                    color=discord.Color.red(),
                )
                em.set_footer(text="Use the command ?todo add [stuff to do] to add something!")
                await ctx.send(embed=em)
            else:
                strtodolist = ""
                for item in todolist:
                    strtodolist += str(todolist.index(item) + 1)
                    strtodolist += f". {item} \n"
                em = discord.Embed(
                    title=f"{ctx.author.name}'s To-Do List", description=strtodolist, color=discord.Color.green()
                )
                em.set_footer(text="Nice to-do list ya got there.")
                await ctx.send(embed=em)
        except:
            fmt = {"todolist": []}
            data[str(ctx.author.id)] = fmt
            with open("database/todolist.json", "w") as f:
                data = json.dump(data, f, indent=4)
            em = discord.Embed(
                title=f"{ctx.author.name}'s To-Do List",
                description="This user has nothing on their to-do list.",
                color=discord.Color.red(),
            )
            em.set_footer(text="Use the command ?todo add [stuff to do] to add something!")
            await ctx.send(embed=em)

    @todo.command(name="add")
    async def addtodo(self, ctx, *, arg):
        with open("database/todolist.json", "r") as f:
            data = json.load(f)
        try:
            data[str(ctx.author.id)]["todolist"].append(arg)
            with open("database/todolist.json", "w") as f:
                data = json.dump(data, f, indent=4)
        except:
            fmt = {"todolist": []}
            data[str(ctx.author.id)] = fmt
            data[str(ctx.author.id)]["todolist"].append(arg)
            with open("database/todolist.json", "w") as f:
                data = json.dump(data, f, indent=4)
        await ctx.send(f"Added `{arg}` to your to-do list :)")

    @todo.command(name="remove")
    async def removetodo(self, ctx, index):
        with open("database/todolist.json", "r") as f:
            data = json.load(f)

        try:
            index = int(index)
            todolist = data[str(ctx.author.id)]["todolist"]
            del todolist[index - 1]
            with open("database/todolist.json", "w") as f:
                data = json.dump(data, f, indent=4)
            await ctx.send("Success")
        except:
            await ctx.send("Looks like there is nothing in your to-do list, or there was an error.")

    @commands.group(name="calc", aliases=["calculator"])
    async def calc(self, ctx):
        """
        A GREAT calculator! Subcommands include **?calc normal**, **?calc combinatorics**, **?calc simplify**, and **?calc trig**. Example: ?calc norm 1 + 1 will return 2
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "You need to provide a valid subcommand. Currently, there is `?calc normal`, `?calc combinatorics`, `?calc simplify`, and `?calc trig`."
            )

    @calc.command(name="normal", aliases=["norm", "basic"])
    async def basic_calc(self, ctx, num1=None, operation=None, num2=None):
        if num1 != None and num2 != None and operation != None:
            num1 = float(num1)
            num2 = float(num2)
            await ctx.send(f"`{num1} {operation} {num2} = {ops[operation](num1,num2)}`")
        else:
            await ctx.send(
                "Invalid formatting, please add a space between the numbers and the operation. For example, `1 + 1` will return 2, while `1+1` will return an error."
            )

    @calc.command(name="trig", aliases=["trigonometry"])
    async def trig_calc(self, ctx, function=None, num=None, num_type="degrees"):
        if function != None and num != None:
            num = float(num)
            if num_type == "degrees":
                num_deg = math.radians(num)
                num_str = str(num) + "°"
            else:
                num_deg = num
                num_str = str(num) + " rad"
            if function in ["sin", "sine", "s"]:
                await ctx.send(f"`sin({num_str}) = {math.sin(num_deg)}`")
            if function in ["cos", "cosine", "c"]:
                await ctx.send(f"`cos({num_str}) = {math.cos(num_deg)}`")
            if function in ["tan", "tangent", "t"]:
                await ctx.send(f"`tan({num_str}) = {math.tan(num_deg)}`")
        else:
            await ctx.send(
                "Invalid formatting, please use this format: \n```?calc trig [function] [number] [type (radians or degrees, default degrees)]``` \n(E.g. `?calc trig sin 90` will return `1.0`)"
            )

    @calc.command(name="c", aliases=["combinatorics", "combinations"])
    async def combinatorics_calc(self, ctx, num1=None, operation=None, num2=None):
        if num1 != None and num2 != None and operation != None:
            num1 = int(num1)
            num2 = int(num2)
            if operation.lower() in ["c", "choose", "combo", "combination"]:
                solution = math.factorial(num1) / (math.factorial(num2) * math.factorial(num1 - num2))
                operation = "choose"
            elif operation.lower() in ["p", "permutate", "permute", "perm", "permutation"]:
                solution = math.factorial(num1) / math.factorial(num1 - num2)
                operation = "permutate"
            else:
                return await ctx.send(
                    "Invalid formatting, please use this format: `5 C 1` for '5 choose 1', or `5 P 1` for permutations."
                )
            await ctx.send(f"`{num1} {operation} {num2} = {solution}`")
        else:
            await ctx.send(
                "Invalid formatting, please use this format: `5 C 1` for '5 choose 1', or `5 P 1` for permutations."
            )

    @calc.command(name="simplify", aliases=["simp", "simple"])
    async def simply_fractions(self, ctx, numerator=None, denominator=None):
        if numerator != None and denominator != None:
            await ctx.send(simplify_fraction(int(numerator), int(denominator)))
        else:
            await ctx.send("Invalid formatting, please use this format: `?calc simplify [numerator] [denominator]`")

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, user: discord.Member = None):
        """
        Sends info about a specific user
        """
        try:
            week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            if user == None:
                user = ctx.author
            id = user.id
            register_date = datetime_from_utc_to_local(user.created_at)
            joined_date = datetime_from_utc_to_local(user.joined_at)
            day_of_week = week_days[register_date.weekday()]
            day_of_week_2 = week_days[joined_date.weekday()]
            month = months[register_date.month - 1]
            month_2 = months[joined_date.month - 1]
            register_date = (
                f"{day_of_week}, {month} {register_date.day}, {register_date.year} {register_date.strftime('%I:%M %p')}"
            )
            joined_date = (
                f"{day_of_week_2}, {month_2} {joined_date.day}, {joined_date.year} {joined_date.strftime('%I:%M %p')}"
            )
            em = discord.Embed(description=user.mention, color=user.color)
            em.set_author(name=f"{user}", icon_url=str(user.avatar_url))
            em.add_field(name="Joined", value=joined_date)
            em.add_field(name="Registered", value=register_date)
            em.add_field(
                name="Basic Info",
                value=f"**User ID**: {id} \n**Name**: {user.name} \n**Discriminator**: {user.discriminator} \n**Nickname**: {user.display_name}",
                inline=False,
            )
            em.add_field(name="Other Stuffs", value=f"**Displayed Color Hex**: {user.color}")
            em.set_thumbnail(url=user.avatar_url)
            em.set_footer(text=f"ID: {id} • Today at {datetime_from_utc_to_local(datetime.now()).strftime('%I:%M %p')}")
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["guildinfo"])
    async def serverinfo(self, ctx):
        """
        Sends info about the guild that the command was sent in
        """
        try:
            guild_id = ctx.guild.id
            guild = self.bot.get_guild(guild_id)
            week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            creation_date = datetime_from_utc_to_local(guild.created_at)
            day_of_week = week_days[creation_date.weekday()]
            month = months[creation_date.month - 1]
            creation_date = (
                f"{day_of_week}, {month} {creation_date.day}, {creation_date.year} {creation_date.strftime('%I:%M %p')}"
            )
            em = discord.Embed(color=ctx.author.color)
            em.set_author(name=f"{guild.name}", icon_url=str(guild.icon_url))
            em.add_field(name="Owner", value=f"{guild.owner}")
            em.add_field(name="Members", value=f"{len(guild.members)}")
            em.add_field(name="Roles", value=f"{len(guild.roles)}")
            em.add_field(name="Text Channels", value=f"{len(guild.text_channels)}")
            em.add_field(name="Voice Channels", value=f"{len(guild.voice_channels)}")
            em.add_field(name="Categories", value=f"{len(guild.categories)}")
            em.add_field(name="Region", value=f"{guild.region}")
            em.add_field(name="Emoji Limit", value=f"{guild.emoji_limit}")
            em.add_field(name="Filesize Limit", value=f"{math.ceil(guild.filesize_limit/1048576)} MB")
            em.add_field(name="Bitrate Limit", value=f"{guild.bitrate_limit}")
            ruleschannel = guild.rules_channel
            if ruleschannel == None:
                ruleschannel = "None"
            em.add_field(name="Rules Channel", value=ruleschannel.mention)
            em.add_field(name="Boosters Role", value=f"{guild.premium_subscriber_role}")
            em.set_thumbnail(url=guild.icon_url)
            em.set_footer(text=f"ID: {guild_id} | Server Created • {creation_date}")
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["wolfram", "wfa", "wa"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def wolframalpha(self, ctx, *, arg):
        """
        Enter a math question, and it will return the result from Wolfram Alpha! It can even do weather! Note: Wolfram Alpha might not always be able to find the answer.
        """
        # Taking input from user
        question = arg

        # App id obtained by the above steps
        app_id = "8UATA8-8945JE29AQ"
        try:
            # Instance of wolf ram alpha
            # client class
            client = wolframalpha.Client(app_id)
            # Stores the response from
            # wolf ram alpha
            res = client.query(question)

            # Includes only text from the response
            answer = next(res.results).text
        except:
            answer = "Couldn't find the answer on Wolfram Alpha."
            await asyncio.sleep(1)

        em = discord.Embed(title="Wolfram Alpha's Response", color=discord.Color.blue())
        em.add_field(name="You asked:", value=question)
        em.add_field(name="Reponse:", value=answer, inline=False)
        await ctx.send(embed=em)

    @commands.command(name="dictionary", aliases=["dict", "def", "define"])
    async def dictionary(self, ctx, *, phrase):
        """
        Shows the definition for a word.
        """
        try:
            result = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{phrase}").json()
            result[0]["word"]
        except:
            return await ctx.send(
                embed=discord.Embed(
                    title="An Error Occurred",
                    description="Sorry, I could not find that word in the dictionary",
                    color=discord.Color.red(),
                )
            )
        try:
            word = result[0]["word"].capitalize()
            pronunciation = result[0]["phonetics"][0]["text"]
            em = discord.Embed(
                title=f"Definition for: {word}",
                description=f"Pronunciation: `{pronunciation}`",
                color=discord.Color.blue(),
            )
            if len(result[0]["meanings"]) > 3:
                for i in range(3):
                    try:
                        example = result[0]["meanings"][i]["definitions"][0]["example"].capitalize()
                    except:
                        example = "None"
                    em.add_field(
                        name=f"Definition {i+1}",
                        value=f"**Definition**: {result[0]['meanings'][i]['definitions'][0]['definition']} \n**Part of Speech**: {result[0]['meanings'][i]['partOfSpeech'].capitalize()} \n**Example**: {example}",
                        inline=False,
                    )
            else:
                for i in range(len(result[0]["meanings"])):
                    try:
                        example = result[0]["meanings"][i]["definitions"][0]["example"].capitalize()
                    except:
                        example = "None"
                    em.add_field(
                        name=f"Definition {i+1}",
                        value=f"**Definition**: {result[0]['meanings'][i]['definitions'][0]['definition']} \n**Part of Speech**: {result[0]['meanings'][i]['partOfSpeech'].capitalize()} \n**Example**: {example}",
                        inline=False,
                    )
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["tr", "trans"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def translate(self, ctx, lang_to, *, arg):
        """
        Translate into another language! Example: **?translate spanish hello**
        """
        colors = [0x4DEEEA, 0x74EE15, 0xFFE700, 0xF000FF]
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            return await ctx.send("You did not provide a valid language!")
        try:
            if lang_to not in googletrans.LANGCODES:
                lang_to = googletrans.LANGUAGES[lang_to]
            translator = Translator()
            text_translated = translator.translate(arg, dest=lang_to).text
            em = discord.Embed(title=f"Translation", description="Penguin is a polyglot.", color=random.choice(colors))
            em.add_field(name="Original Entry", value=f"`{arg}`")
            em.add_field(name=f"Translated Into {lang_to.title()}", value=f"`{text_translated}`", inline=False)
            langs = translator.detect(arg)
            em.set_footer(
                text=f"Translated from {googletrans.LANGUAGES[langs.lang.lower()].title()}, with confidence {langs.confidence*100}%"
            )
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong! {:.1f} ms".format(self.bot.latency * 1000))

    @commands.command(name="random", aliases=["ran", "rand"])
    async def random_num(self, ctx, num1, num2):
        """
        Send two numbers, and Penguin will pick a random number between them, inclusive.
        """
        try:
            num1 = int(num1)
            num2 = int(num2)
            await ctx.send(
                embed=discord.Embed(
                    title=f"Random Number from {num1} to {num2}",
                    description=f"I Choose: `{random.randint(num1, num2)}`",
                    color=discord.Color.green(),
                )
            )
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Error!",
                    description="You didn't provide valid numbers! Also make sure you provide them in increasing order!",
                    color=discord.Color.red(),
                )
            )

    @commands.command(name="pick", aliases=["choose"])
    async def pick(self, ctx, *args):
        """
        Send a list in this format: ?pick [object 1] [object 2] [object 3] and Penguin will pick an object from the list.
        """
        if args is None:
            return await ctx.send("You didn't send anything to pick from!")
        items = [arg for arg in args]
        await ctx.send(
            embed=discord.Embed(
                title="What Does Penguin Pick?",
                description=f"I Pick: `{random.choice(items)}`",
                color=discord.Color.green(),
            )
        )

    @commands.command(name="afk", aliases=["gone", "away"])
    async def afk(self, ctx, *reason):
        """
        If you are going AFK, you can turn use this command so that people know you're gone.
        """
        if reason == None:
            return await ctx.send("Please provide a reason so that people know why.")
        reason = " ".join(reason)
        with open("database/utility.json", "r") as f:
            data = json.load(f)
        try:
            if data[str(ctx.author.id)]["reason"] is not None:
                return await ctx.reply(
                    "You already have AFK as **ENABLED**! Use `?afkoff` to indicate that you're back!",
                    mention_author=False,
                )
        except:
            pass
        try:
            fmt = {"reason": reason, "starttime": str(datetime.now())}
            data[str(ctx.author.id)] = fmt
            with open("database/utility.json", "w") as f:
                data = json.dump(data, f, indent=4)
            await ctx.send(
                embed=discord.Embed(
                    title="Goodbye!",
                    description="You now have set your AFK status as **ON**. When you return, please use the command `?afkoff` to indicate that you're back.",
                    color=discord.Color.blurple(),
                )
            )
        except:
            traceback.print_exc()

    @commands.command()
    async def afkoff(self, ctx):
        """
        Turns off your AFK, indicating that you're back.
        """
        try:
            with open("database/utility.json", "r") as f:
                data = json.load(f)
            starttime = data[str(ctx.author.id)]["starttime"]
            starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
            if data[str(ctx.author.id)]["reason"] is None:
                return await ctx.reply("You were never AFK in the first place!", mention_author=False)
            else:
                fmt = {"reason": None, "starttime": None}
                data[str(ctx.author.id)] = fmt
                with open("database/utility.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                now = datetime.now()
                await ctx.send(
                    embed=discord.Embed(
                        title="Welcome Back!",
                        description=f"You were gone for {clean_time((now - starttime).total_seconds())}",
                        color=discord.Color.blurple(),
                    )
                )
        except:
            traceback.print_exc()

    @commands.command(name="binarytostring", aliases=["bts", "btostring", "btos"])
    async def convert_binary(self, ctx, *, arg):
        """
        Decodes binary input into readable text.
        """
        converted = decode_binary_string(arg)
        if converted == "":
            await ctx.send("There was an error, make sure it's in binary.")
        try:
            await ctx.send(
                embed=discord.Embed(
                    title="Binary to String",
                    description=f"Converted from binary to string: `{converted}`",
                    color=discord.Color.green(),
                )
            )
        except:
            await ctx.send("There was an error, make sure it's in binary.")

    @commands.command(name="displaywithcolor", aliases=["dwc", "colordisplay", "cdisplay"])
    async def display_with_color(self, ctx, hex_str="0x000000"):
        """
        Displays an embed with the specified hex code as its color.
        """
        try:
            hex_value = int(hex_str, 16)
            await ctx.send(
                embed=discord.Embed(
                    title="This is an embed", description="The color should be the provided hex code", color=hex_value
                )
            )
        except:
            await ctx.send("Not a valid hex")

    @commands.command(name="getcolor", aliases=["gcolor", "getc"])
    async def get_color(self, ctx, role: discord.Role = None):
        """
        Gets the hex code of a role.
        """
        if role is None:
            return await ctx.send("Bruh, you can't do that with no role.")
        await ctx.send(
            embed=discord.Embed(
                title=f"Color Used For Role: {role.name}",
                description=f"Hex Code: {role.color} \nThe embed should be displayed with the color of the role.",
                color=role.color,
            )
        )

    @commands.command(name="getembedcolor", aliases=["gec"])
    async def get_embed_color(self, ctx, message_id):
        """
        Returns the color of the embed in a message given message id.
        """
        channel = self.bot.get_channel(ctx.channel.id)
        message = await channel.fetch_message(message_id)
        try:
            embeds = message.embeds
            await ctx.send(
                f"Hex Code for the message: {embeds[0].color} \nhttps://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
            )
        except:
            await ctx.send("No embeds in that message.")

    @commands.command()
    async def score(self, ctx, *team):
        """
        Displays the most recent score of an NBA game given the team, credits to ESPN.
        """
        team = " ".join(team)
        scoreboard = espn_scoreboard.ESPNScoreboard("basketball", "nba")
        now = datetime.now().strftime("20%y%m%d")
        int_now = int(now)
        initial_int_now = int_now
        score_received = False
        while score_received is False:
            if initial_int_now - int_now > 10:
                return await ctx.send("Couldn't find a recent score for that team.")
            now = str(int_now)
            scores = scoreboard.get_scoreboard(now)
            for event in scores["events"]:
                for competition in event.competitions:
                    competitors = competition.competitors

                    team1 = competitors[0]
                    team2 = competitors[1]
                    if team.lower() in [
                        team1.team.display_name.lower(),
                        team2.team.display_name.lower(),
                        team1.team.abbreviation.lower(),
                        team2.team.abbreviation.lower(),
                        team1.team.short_display_name.lower(),
                        team2.team.short_display_name.lower(),
                    ]:
                        competition_date = competition.date.replace("T", " ").replace("Z", "").split(" ")[0]
                        description = f"{competition.status.display_clock} left in Q{competition.status.period}"
                        if competition.status.display_clock == "0.0":
                            description = "Game Has Ended"
                        if (
                            team1.score > team2.score
                            and team.lower()
                            in [
                                team1.team.display_name.lower(),
                                team1.team.abbreviation.lower(),
                                team1.team.short_display_name.lower(),
                            ]
                        ) or (
                            team2.score > team1.score
                            and team.lower()
                            in [
                                team2.team.display_name.lower(),
                                team2.team.abbreviation.lower(),
                                team2.team.short_display_name.lower(),
                            ]
                        ):
                            color = discord.Color.green()
                        elif team1.score == team2.score:
                            color = discord.Color.blurple()
                        else:
                            color = discord.Color.red()
                        em = discord.Embed(
                            title=f"{team1.team.display_name} VS {team2.team.display_name}",
                            description=description,
                            color=color,
                        )
                        em.add_field(
                            name="Score",
                            value=f"{team1.team.display_name}: {team1.score} \n {team2.team.display_name}: {team2.score}",
                        )
                        em.add_field(name="\u2800", value="\u2800")
                        em.add_field(name="Date", value=competition_date)
                        em.add_field(
                            name=f"Team Stats - {competitors[0].team.abbreviation}",
                            value=f"{competitors[0].statistics[0].display_value} {competitors[0].statistics[0].name} \n{competitors[0].statistics[2].display_value} {competitors[0].statistics[2].name}",
                            inline=False,
                        )
                        # em.add_field(name = "\u2800", value = "\u2800")
                        em.add_field(
                            name=f"Team Stats - {competitors[1].team.abbreviation}",
                            value=f"{competitors[1].statistics[0].display_value} {competitors[1].statistics[0].name} \n{competitors[1].statistics[2].display_value} {competitors[1].statistics[2].name}",
                        )
                        em.set_footer(
                            text=f"Location: {competition.venue.address_city}, {competition.venue.address_state}"
                        )
                        await ctx.send(embed=em)
                        score_received = True
            int_now -= 1

    @commands.command()
    async def scoreboard(self, ctx):
        """
        Displays the NBA scoreboard for all games today
        """
        try:
            scoreboard = espn_scoreboard.ESPNScoreboard("basketball", "nba")
            now = datetime.now().strftime("20%y%m%d")
            scores = scoreboard.get_scoreboard(now)
            description = ""
            for event in scores["events"]:
                for competition in event.competitions:
                    competitors = competition.competitors

                    team1 = competitors[0]
                    team2 = competitors[1]
                    time_left = f"{competition.status.display_clock} left in Q{competition.status.period}"
                    if time_left == "0.0 left in Q0":
                        time_left = "Game Has Not Started"
                    if time_left == "0.0 left in Q4":
                        time_left = "Final"
                    description += f"**{team1.team.display_name} - {team1.score}, {team2.team.display_name} - {team2.score}** | {time_left}\n\n"
            em = discord.Embed(title="NBA Games Today", description=description, color=discord.Color.green())
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["wiki"])
    async def wikipedia(self, ctx, *args):
        """
        Enters the query into Wikipedia and looks for an answer.
        """
        search = " ".join(args)
        try:
            # async with ctx.typing(): <- Still typing after sent for some reason
            wikipage = wikipedia.page(search)
            em = discord.Embed(
                title=search.title(), description=wikipedia.summary(search, sentences=5), color=discord.Color.green()
            )
            if len(wikipage.images) > 0:
                em.set_thumbnail(url=wikipage.images[0])
            await ctx.send(embed=em)
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Error!",
                    description=f"Could not find `{search}` on Wikipedia. Please try something else.",
                    color=discord.Color.red(),
                )
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "?afk" in message.content.lower() and message.content.lower() != "?afkoff":
            return
        with open("database/utility.json", "r") as f:
            data = json.load(f)
        # if '<@!' in message.content:
        for id in data:
            user = self.bot.get_user(int(id))
            if user.mentioned_in(message) and data[id]["starttime"] is not None:
                await message.channel.send(
                    content=message.author.mention,
                    embed=discord.Embed(
                        title="DUDE! CHILL!",
                        description=f"<@!{id}> is away currently! Please do not ping them! They are away for the following reason: **{data[id]['reason']}**",
                        color=discord.Color.red(),
                    ),
                )
                await user.send(
                    embed=discord.Embed(
                        title=f"You were pinged in {message.guild.name} while AFK!",
                        description=f"{message.author.name} Pinged You \n Message Content: {message.content}",
                        color=discord.Color.dark_gold(),
                    )
                )
        if str(message.author.id) in data and data[str(message.author.id)]["starttime"] is not None:
            await message.channel.send(
                "I've noticed that you're back... do you want to turn AFK off? The command is `?afkoff`."
            )
        if (
            "gtg" in message.content.lower()
            or "i hafta go" in message.content.lower()
            or "i have to go" in message.content.lower()
            or "i gotta go" in message.content.lower()
            or "i needa go" in message.content.lower()
        ):
            if str(message.author.id) not in data or data[str(message.author.id)]["starttime"] is None:
                await message.channel.send("Do you want to enable AFK? You can do `?afk [reason]`")

        # if len(message.attachments) > 0:
        #     user = self.bot.get_user(541482948155670548)
        #     await user.send(f"Sent by: {message.author} \n{message.attachments[0].url}") #####WOULD SEND ME THE ATTACHMENT


def setup(bot):
    bot.add_cog(Utility(bot))
