import asyncio
import json
import random
import traceback

import aiohttp
import discord
import requests
from akinator.async_aki import Akinator
from discord.ext import commands
from discord.ext.commands import MemberConverter


def random_color():
    return random.randint(0, 0xFFFFFF)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return json_data[0]["q"] + " -" + json_data[0]["a"]


class Fun(commands.Cog):
    """The funnest commands on planet Earth!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"])
    async def fortune(self, ctx, *, arg):
        """8-ball command! Ask Penguin any question, and it will give you its response."""
        if "curry" in arg.lower():
            answer = "Curry will win the MVP this year and end his career with 6 rings."
        elif "warriors" in arg.lower():
            answer = "Warriors are gonna be champs next year, 100%"
        elif "klay" in arg.lower():
            answer = "Klay is gonna average 25 ppg upon returning from injury."
        else:
            answers = [
                "yes",
                "no",
                "maybe",
                "Bro don't ask me",
                "Ye fosho",
                "Definite no.",
                "Why ask me?",
                "Ofc",
                "Nah",
                "Ask Kool",
                "Idk",
                "Meh",
            ]
            answer = random.choice(answers)
        await ctx.send(answer)

    @commands.command()
    async def slap(self, ctx, arg, *, reason):
        """A member is being mean to you? SLAP them using this command! :)"""

        embed = discord.Embed(
            title="Slap", description=f"{ctx.author} slapped {arg} because **{reason}**", color=0x006BB6
        )
        embed.set_image(url="https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def cry(self, ctx):
        """Are you feeling sad? Use this command to cry until you aren't sad anymore! You even get one coin! :D"""
        user = ctx.author
        embed = discord.Embed(title=f"{user} cries.", description="Here, take 1 coin. JK", color=0x006BB6)
        embed.set_image(url="https://media.giphy.com/media/d2lcHJTG5Tscg/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=["hf", "highfive", "high5"])
    async def high_five(self, ctx, arg):
        """Got the job done with a teammate? High-five them!"""
        embed = discord.Embed(title="High Five", description=f"{ctx.author} high-fived {arg}", color=0x006BB6)
        embed.set_image(url="https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def bully(self, ctx, arg, *, reason):
        """Feel like bullying someone? Use this command!"""
        embed = discord.Embed(title="Bully", description=f"{ctx.author} bullied {arg} for **{reason}**", color=0x006BB6)
        embed.set_image(url="https://media.giphy.com/media/3UgqexCoCIFdS/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, arg, *, reason):
        """Someome did a good job? Pat them!"""

        embed = discord.Embed(title="Pat", description=f"{ctx.author} pats {arg} for **{reason}**", color=0x006BB6)
        embed.set_image(url="https://media.giphy.com/media/M3a51DMeWvYUo/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def poke(self, ctx, arg, *, reason):
        """Is someone not responding to you? Poke them and annoy them until they do! >:D"""
        embed = discord.Embed(title="Poke", description=f"{ctx.author} pokes {arg} for **{reason}**", color=0x006BB6)
        embed.set_image(url="https://media.giphy.com/media/8PBC5GXof1G7iODApJ/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def apologize(self, ctx, arg, *, reason):
        """Did something to someone that you deeply regret? You can always apologize and hope for forgiveness! Just use this command!"""
        embed = discord.Embed(
            title="Apologize",
            description=f"{ctx.author} apologizes to {arg}. \nApology message: **{reason}**",
            color=0x006BB6,
        )
        embed.set_image(url="https://media.giphy.com/media/U3n0oczF7jByEnhXAR/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def inspire(self, ctx):
        """Want to be inspired? This command uses an API to give you inspirational quotes! Look at Penguin man, so inspirational!"""
        quote = get_quote()
        await ctx.send(quote)

    @commands.command()
    async def kill(self, ctx, member: discord.Member = None):
        """Welllll, in the rare occassion that you want to kill someone (this is 100% for fun), you can use this command, and it will send a random message on how the person targeted dies."""
        killmsg = random.choice(
            [
                f"{member} ate yellow snow and died.",
                f"{member} sat on an icicle and died. :eyes:",
                f"{member} mentioned the PCC in front of Prim and was burnt alive by her. :fire:",
                f"{member} was boxed like a fish, leading to death.",
                f"{member} was mauled by a polar bear. RIP.",
                f"{member} died from hypothermia after staying in the arctic for too long.",
                f"{member} drowned to death while streaming themselves diving into the freezing arctic ocean. :cold_face:",
                f"An iceberg fell out of the sky and bonked {member} on their head",
            ]
        )
        await ctx.send(killmsg)

    @commands.command()
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Wanna ship two people? Use this command to see how compatible they are? Maybe they're not fit for each other. But maybe they are 100% PERFECT together! :eyes: :heart:"""

        if user1 == user2:
            return await ctx.send("You can't ship the same person!")

        compatibility = random.randint(1, 100)
        if compatibility > 0 and compatibility < 25:
            message = "Not a good match. :broken_heart:"
        if compatibility > 24 and compatibility < 50:
            message = "Decent. :heart:"
        if compatibility > 49 and compatibility < 75:
            message = "They should date. :sparkling_heart:"
        if compatibility > 74 and compatibility < 90:
            message = "Lovebirds. :kissing_heart:"
        if compatibility > 89 and compatibility < 101:
            message = "Most likely, they are already married. :gift_heart:"
        embed = discord.Embed(
            title=":heartpulse: Matchmaking :heartpulse:",
            description=f"`{user1}x{user2}`? \n\n{user1} and {user2} are {compatibility}% compatible. {message}",
            color=0xFFB6C1,
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def game(self, ctx):
        """A simple game that anyone can start, first to react wins!"""
        await ctx.message.delete()
        msg = await ctx.send("React first to win")
        await msg.add_reaction("👍")

        def check(reaction, user):
            return str(reaction.emoji) == "👍" and user != self.bot.user

        try:
            # Timeout parameter is optional but sometimes can be useful
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)

            # Will wait until a user reacts with the specified checks then continue on with the code
            await ctx.send(f"Congratulations {user.name} you won!")
        except asyncio.TimeoutError:
            # when wait_for reaches specified timeout duration (in this example it is 30 seconds)
            await ctx.send("You ran out of time!")

    @commands.command()
    async def mock(self, ctx, *, arg):
        """Enter a random phrase, and the bot will respond with the same phrase, but in a mocking kind of way!"""
        new_str = ""
        for i in range(len(arg)):
            letter = arg[i]
            letter = letter.lower() if i % 2 == 0 else letter.upper()
            new_str += letter
        await ctx.send(new_str)

    @commands.command()
    async def prim(self, ctx, *, arg):
        """Enter a random phrase, and the bot will respond with the same phrase, but talk like Prim!"""
        rand = random.randint(1, 8)
        new_str = arg
        if "hello" in new_str.lower():
            new_str = new_str.replace("hello", "henlo")
            new_str = new_str.replace("Hello", "Henlo")
            new_str = new_str.replace("HELLO", "HENLO")
        if "hi" in new_str.lower():
            new_str = new_str.replace("hi", "henlo")
            new_str = new_str.replace("Hi", "Henlo")
            new_str = new_str.replace("HI", "HENLO")
        if "good" in new_str.lower():
            new_str = new_str.replace("good", "gouda")
            new_str = new_str.replace("Good", "Gouda")
            new_str = new_str.replace("GOOD", "GOUDA")
        if "lol" in new_str.lower():
            new_str = new_str.replace("lol", "lols")
            new_str = new_str.replace("Lol", "Lols")

        if rand == 1:
            new_str += " lols"
        elif rand == 2:
            new_str += " lols XD"
        elif rand == 3:
            new_str += "-"
        elif rand == 4:
            new_str += " XDDDDDDDD"
        elif rand == 5:
            new_str += " XD"
        elif rand == 6:
            new_str = "<:woke:809493457617944586>"
        elif rand == 7:
            new_str += " ***W H E E Z E***"
        else:
            new_str = "<:SHUT:829821900561449071>"

        new_str = new_str[0].upper() + new_str[1:]
        await ctx.send(new_str)

    @commands.command(name="rice", aliases=["whostolemyrice", "whostole", "wsmr"])
    async def rice(self, ctx, *, arg):
        """Enter a random phrase, and the bot will respond with the same phrase, but with some *slight* modifications to imitate the way that Whostolemyrice types!"""
        new_str = ""
        rand = random.randint(1, 3)
        if rand == 1:
            new_str = "nice"
        elif rand == 2:
            new_str = "<:BADLANDS:824396043349131275>"
        else:
            new_str = f"bruh {arg}"
        await ctx.send(new_str)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def wordgame(self, ctx):  # sourcery no-metrics
        """Literally the best game ever created, you take turns, and whoever's turn it is, they will have a certain amount of time to think of a word that contains a certain 3 letters. No repeats!"""
        combinations = [
            "con",
            "ion",
            "tim",
            "ins",
            "tel",
            "lie",
            "ake",
            "ace",
            "fac",
            "ext",
            "dan",
            "per",
            "ect",
            "cal",
            "for",
            "sim",
            "pin",
            "sta",
            "eno",
            "sab",
            "ait",
            "lat",
            "fec",
            "fic",
            "ict",
            "ake",
            "ine",
            "ane",
            "ade",
            "emo",
            "low",
            "exo",
            "for",
            "non",
        ]
        penguin_channel = self.bot.get_channel(ctx.channel.id)
        hooks = await penguin_channel.webhooks()
        hook = discord.utils.get(hooks, name="Penguin")

        if not hook:
            url = "https://cdn.discordapp.com/app-icons/783216602849607681/1343d0b9c0195a11c7b2f0160aaacd16.png?size=32&keep_aspect_ratio=false"
            async with aiohttp.ClientSession().get(url) as resp:
                im = await resp.read()

            hook = await ctx.channel.create_webhook(name="Penguin", avatar=im)

        streak = 0
        players = []
        await hook.send(
            "Game is starting! Say `?join` to join! Whoever started the game will say `?start` to officially start the game!"
        )
        while True:
            response = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel)
            if response.content == "?cancel":
                await hook.send("Cancelling...")
                with open("database/wordgame.json", "r") as f:
                    data = json.load(f)
                data = {}
                with open("database/wordgame.json", "w") as f:
                    json.dump(data, f)
                return
            if response.content == "?join":
                await hook.send(f"Added {response.author} to the game!")
                fmt = {"strikes": 0, "name": str(response.author.name), "userid": response.author.id}
                with open("database/wordgame.json", "r") as f:
                    data = json.load(f)

                user_name = str(response.author)

                # user_id = str(user_id)
                data[user_name] = fmt

                with open("database/wordgame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
            elif response.content == "?start":
                if response.author == ctx.author:
                    await hook.send("Starting game...")
                    break
                else:
                    pass

        # await ctx.send("Time's up! Let's start!")
        await asyncio.sleep(1)
        with open("database/wordgame.json", "r") as f:
            data = json.load(f)
        try:
            for userid in data:
                players.append(userid)
            # print(*players, sep = ", ")
            playerlist = "[{0}]".format(", ".join(map(str, players))).replace("[", "").replace("]", "")
            await hook.send(f"Starting a word game with `{playerlist}`")
            with open("database/wordgame.json", "w") as f:
                json.dump(data, f)
        except:
            traceback.print_exc()
        try:
            with open("database/wordgame.json", "r") as f:
                data = json.load(f)
            # x = 0
            usedwords = []
            gamegoing = True
            while gamegoing == True:
                description = ""
                for z in players:
                    description += f"{z}: {data[z]['strikes']} \n\n"
                em = discord.Embed(title="Strikes so far", description=f"{description}", color=random_color())
                await hook.send(embed=em)
                await asyncio.sleep(2)
                for player in players:
                    with open("database/wordgame.json", "r") as f:
                        data = json.load(f)
                    id = str(data[player]["userid"])
                    await hook.send(f"<@!{id}>")
                    done = False
                    while done == False:
                        combination = random.choice(combinations)
                        em = discord.Embed(
                            title=f"{player}'s Turn",
                            description=f"Think of a word containing `{combination}`",
                            color=random_color(),
                        )
                        em.set_footer(text=f"🔥 Streak: {streak}")
                        await hook.send(embed=em)
                        converter = MemberConverter()
                        player_ = await converter.convert(ctx, player)

                        def check(m):
                            return m.channel == ctx.channel and m.author == player_ and not m.content.startswith(".")

                        try:
                            res = await self.bot.wait_for("message", check=check, timeout=15.0)
                        except asyncio.TimeoutError:
                            streak = 0
                            data[player]["strikes"] += 1
                            await hook.send(
                                f"Rip. You didn't think of something in time. You now have {data[player]['strikes']} strikes."
                            )
                            with open("database/wordgame.json", "w") as f:
                                json.dump(data, f)
                            done = True
                            break
                        if res.content == "?cancel":
                            await hook.send("Cancelling...")
                            with open("database/wordgame.json", "r") as f:
                                data = json.load(f)
                            data = {}
                            with open("database/wordgame.json", "w") as f:
                                json.dump(data, f)
                            return
                        if combination in res.content.lower():
                            try:
                                result = requests.get(
                                    f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{res.content.lower()}"
                                ).json()
                                result[0]["word"]
                            except:
                                streak = 0
                                data[player]["strikes"] += 1
                                with open("database/wordgame.json", "w") as f:
                                    json.dump(data, f)
                                await hook.send(
                                    f"That word doesn't exist! You now have {data[player]['strikes']} strikes."
                                )
                                done = True
                                break
                            if res.content.lower() in usedwords:
                                streak = 0
                                data[player]["strikes"] += 1
                                await hook.send(
                                    f"That word has already been used! Because this is a hard game, I shall give you a strike. You now have {data[player]['strikes']} strikes."
                                )
                                with open("database/wordgame.json", "w") as f:
                                    json.dump(data, f)
                                done = True
                                break
                            await res.add_reaction("✅")
                            usedwords.append(res.content.lower())
                            streak += 1
                            # await ctx.send("NICE! That word works!")
                            done = True
                        else:
                            streak = 0
                            data[player]["strikes"] += 1
                            with open("database/wordgame.json", "w") as f:
                                json.dump(data, f)
                            await hook.send(
                                f"Sorry, that word does not contain `{combination}`. You now have {data[player]['strikes']} strikes."
                            )
                            done = True
                    if data[player]["strikes"] == 3:
                        await hook.send(f"{player} was disqualified because they reached 3 strikes.")
                        with open("database/wordgame.json", "r") as f:
                            data = json.load(f)
                        del data[player]
                        await asyncio.sleep(1)
                        with open("database/wordgame.json", "w") as f:
                            json.dump(data, f)
                        players.remove(player)
                        done = True
                    if len(players) == 1:
                        winner = await converter.convert(ctx, players[0])
                        em = discord.Embed(
                            title="Game Over",
                            description=f"Nice, nice. <@!{winner.id}> is the winner. Hope y'all had fun!",
                            color=discord.Color.green(),
                        )
                        await hook.send(embed=em)
                        with open("database/wordgame.json", "r") as f:
                            data = json.load(f)
                        data = {}
                        with open("database/wordgame.json", "w") as f:
                            json.dump(data, f)
                        done = True
                        gamegoing = False
                        break
        except:
            traceback.print_exc()

        resp.close()

    @commands.command(name="akinator", aliases=["aki"])
    async def akinator_game(self, ctx):  # sourcery no-metrics
        """
        Think of a character, and the bot will ask you some questions. The bot will then guess who that character is! Actually works pretty well.
        """
        aki = Akinator()
        first = await ctx.send("Processing...")
        q = await aki.start_game()

        game_embed = discord.Embed(
            title=f"{str(ctx.author.name)}'s game of Akinator",
            description=q,
            url=r"https://en.akinator.com/",
            color=discord.Color.blurple(),
        )

        game_embed.set_footer(text=f"Wait for the bot to add reactions before you give your response.")

        option_map = {"✅": "y", "❌": "n", "🤷‍♂️": "p", "😕": "pn", "⁉️": "i"}
        """You can pick any emojis for the responses, I just chose what seemed to make sense.
        '✅' -> YES, '❌'-> NO, '🤷‍♂️'-> PROBABLY YES, '😕'-> PROBABLY NO, '⁉️'->IDK, '😔'-> force end game, '◀️'-> previous question"""

        def option_check(reaction, user):  # a check function which takes the user's response
            return user == ctx.author and reaction.emoji in ["◀️", "✅", "❌", "🤷‍♂️", "😕", "⁉️", "😔"]

        await first.delete()  # deleting the message which said "Processing.."
        game_message = await ctx.send(embed=game_embed)
        for emoji in ["◀️", "✅", "❌", "🤷‍♂️", "😕", "⁉️", "😔"]:
            await game_message.add_reaction(emoji)
        # this is aki's certainty level on an answer, per say. 80 seems to be a good number.  EDIT: Changed (Raised) to 85
        while aki.progression <= 85:
            try:

                # taking user's response
                option, _ = await self.bot.wait_for("reaction_add", check=option_check)
                # there might be a better way to be doing this, but this seemed the simplest.
                if option.emoji == "😔":
                    break
                    return await ctx.send("Game ended.")
                # async with ctx.channel.typing():
                if option.emoji == "◀️":  # to go back to previous question
                    try:
                        q = await aki.back()
                    except:  # excepting trying-to-go-beyond-first-question error
                        pass
                    # editing embed for next question
                    game_embed = discord.Embed(
                        title=f"{str(ctx.author.name)}'s game of Akinator",
                        description=q,
                        url=r"https://en.akinator.com/",
                        color=discord.Color.blurple(),
                    )
                    game_embed.set_footer(text=f"{aki.progression}% guessed")
                    # continue
                else:
                    q = await aki.answer(option_map[option.emoji])
                    # editing embed for next question
                    game_embed = discord.Embed(
                        title=f"{str(ctx.author.name)}'s game of Akinator",
                        description=q,
                        url=r"https://en.akinator.com/",
                        color=discord.Color.blurple(),
                    )
                    game_embed.set_footer(text=f"{aki.progression}% guessed")
                    # continue
                await game_message.edit(embed=game_embed)

            except:
                traceback.print_exc()

        await aki.win()

        result_embed = discord.Embed(title="My guess....", colour=discord.Color.dark_blue())
        result_embed.add_field(
            name=f"My first guess is **{aki.first_guess['name']}**", value=aki.first_guess["description"], inline=False
        )
        result_embed.set_footer(text="Was I right? Add the reaction accordingly.")
        result_embed.set_image(url=aki.first_guess["absolute_picture_path"])
        result_message = await ctx.send(embed=result_embed)
        for emoji in ["✅", "❌"]:
            await result_message.add_reaction(emoji)

        option, _ = await self.bot.wait_for("reaction_add", check=option_check, timeout=15)
        if option.emoji == "✅":
            final_embed = discord.Embed(title="I'm a genius", color=discord.Color.green())
        elif option.emoji == "❌":
            final_embed = discord.Embed(title="Oof", description="Maybe try again?", color=discord.Color.red())
        # this does not restart/continue a game from where it was left off, but you can program that in if you like.

        return await ctx.send(embed=final_embed)

    @commands.command(name="fight", aliases=["battle"])
    async def fight(self, ctx, user: discord.Member = None):
        # sourcery no-metrics
        with open("database/fight.json", "r") as f:
            fight = json.load(f)
        if str(ctx.author.id) in fight:
            return await ctx.send("You're already in a fight!")
        if user is None:
            return await ctx.send("You need to specify a user to fight!")
        if user == ctx.author:
            return await ctx.send("You can't fight yourself!")
        msg = await ctx.send(
            f"{user.mention}, {ctx.author.name} is requesting a fight with you! Click the check mark if you want to fight."
        )

        def option_check(reaction, user1):
            return user1 == user and reaction.emoji == "✅"

        for emoji in ["✅"]:
            await msg.add_reaction(emoji)
        try:
            res = await self.bot.wait_for("reaction_add", check=option_check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send(f"{user.name} did not accept in time! The fight was cancelled.")
            return
        fmt = {"health": 100}

        fight[str(ctx.author.id)] = fmt
        fight[str(user.id)] = fmt
        with open("database/fight.json", "w") as f:
            fight = json.dump(fight, f, indent=4)
        with open("database/fight.json", "r") as f:
            fight = json.load(f)
        counter = 0
        while str(ctx.author.id) in fight:
            try:
                if counter % 2 == 0:
                    turn = ctx.author
                    notturn = user
                else:
                    turn = user
                    notturn = ctx.author
                await ctx.send(
                    content=f"{turn.mention}",
                    embed=discord.Embed(
                        title="What do you do?",
                        description="Type `p` for punch - (10 to 35 damage) \n Type `h` for hide - (Gives you time to heal, but you can still be caught) \n Type `pow` for power (40-75 damage if successful)! \n Type `b` for blast (Random amount of damage done to BOTH fighters) \n Type `op` for overpower - (10% chance of setting opponent's health to 10, otherwise, you lose 10 health) \n Type `uh` for ultraheal - (Heals both you and your opponent by the same amount)",
                        color=discord.Color.blurple(),
                    ),
                )

                def check(m):
                    return m.channel == ctx.channel and m.author == turn

                try:
                    res = await self.bot.wait_for("message", check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send(
                        f"{turn.mention} You took too long to think of a decision, and {notturn.name} punched you until you fainted! **GG, {notturn.name} wins!**"
                    )
                    del fight[str(ctx.author.id)]
                    del fight[str(user.id)]
                    with open("database/fight.json", "w") as f:
                        fight = json.dump(fight, f, indent=4)
                    return
                if res.content.lower() in ["p", "punch"]:
                    damage = random.randint(10, 35)
                    await ctx.send(f"You take a huge punch at {notturn.name}, and they lose {damage} damage!")
                    fight[str(notturn.id)]["health"] -= damage
                elif res.content.lower() in ["h", "hide"]:
                    success = random.randint(1, 2)
                    if success == 1:
                        heal = random.randint(1, 25)
                        await ctx.send(
                            f"You climb behind a trash can and pray for the best. Whew! {notturn.name} didn't find you! You manage to gain {heal} health in the process!"
                        )
                        fight[str(turn.id)]["health"] += heal
                    else:
                        damage = random.randint(1, 30)
                        await ctx.send(
                            f"You climb behind a trash can and pray for the best... NOOOOOOOO! {notturn.name} spots you and with a smirk on their face, they punch you. You lose {damage} health!"
                        )
                        fight[str(turn.id)]["health"] -= damage
                elif res.content.lower() in ["pow", "power"]:
                    success = random.randint(1, 3)
                    if success == 1:
                        damage = random.randint(40, 75)
                        await ctx.send(
                            f"Nice! You land a HUGE hit on {notturn.name}, and they look like they're about to faint! They lose {damage} health!"
                        )
                        fight[str(notturn.id)]["health"] -= damage
                    else:
                        damage = random.randint(1, 15)
                        await ctx.send(
                            f"Rip, your punch only skims {notturn.name}'s face, and they barely lose any health. They lose {damage} health."
                        )
                        fight[str(notturn.id)]["health"] -= damage
                elif res.content.lower() in ["b", "blast"]:
                    totaldamage = random.randint(15, 60)
                    damagetouser = random.randint(1, totaldamage)
                    damagetonotuser = totaldamage - damagetouser
                    await ctx.send(
                        f"The blast does **{totaldamage}** damage total. `{damagetouser}` was inflicted upon **{turn.name}**, while `{damagetonotuser}` was inflicted upon **{notturn.name}**"
                    )
                    fight[str(notturn.id)]["health"] -= damagetonotuser
                    fight[str(turn.id)]["health"] -= damagetouser
                elif res.content.lower() in ["op", "overpower"]:
                    rand = random.randint(1, 10)
                    if rand == 4:
                        fight[str(notturn.id)]["health"] = 10
                        await ctx.send(f"YES! {notturn.name}'s health was set to 10. It was **successful**!")
                    else:
                        fight[str(turn.id)]["health"] -= 10
                        await ctx.send("It was **unsuccessful**, and you lose 10 health.")
                elif res.content.lower() in ["uh", "ultraheal"]:
                    heal = random.randint(5, 20)
                    await ctx.send(f"Both you and your opponent healed by {heal} health!")
                    fight[str(notturn.id)]["health"] += heal
                    fight[str(turn.id)]["health"] += heal
                else:
                    await ctx.send("That's not valid! Your turn is skipped.")
                await ctx.send(
                    embed=discord.Embed(
                        title="Health Left",
                        description=f"{ctx.author.name}: {fight[str(ctx.author.id)]['health']} \n{user.name}: {fight[str(user.id)]['health']}",
                    )
                )
                await asyncio.sleep(2)
                if fight[str(ctx.author.id)]["health"] <= 0:
                    await ctx.send(
                        f"{ctx.author.name} was knocked out! **{user.name} wins with {fight[str(user.id)]['health']} health left!**"
                    )
                    del fight[str(ctx.author.id)]
                    del fight[str(user.id)]
                elif fight[str(user.id)]["health"] <= 0:
                    await ctx.send(
                        f"{user.name} was knocked out! **{ctx.author.name} wins with {fight[str(ctx.author.id)]['health']} health left!**"
                    )
                    del fight[str(ctx.author.id)]
                    del fight[str(user.id)]
                with open("database/fight.json", "w") as f:
                    fight = json.dump(fight, f, indent=4)
                with open("database/fight.json", "r") as f:
                    fight = json.load(f)
                counter += 1
            except:
                traceback.print_exc()


def setup(bot):
    bot.add_cog(Fun(bot))
