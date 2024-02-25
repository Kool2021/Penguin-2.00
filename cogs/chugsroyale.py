import asyncio
import json
import math
import random
import traceback

import discord
from discord import Spotify
from discord.ext import commands, menus

bj_userinfo = {}
coin = "<:badlands_coin:831628523180916736>"

default_color_palette = [0x66FF00, 0x1974D2, 0x08E8DE, 0xFFF000, 0xFFAA1D, 0xFF007F]
warriors_color_palette = [0x006BB6, 0xFDB927]
balanced_color_palette = [0xE27D60, 0x85DCB, 0xE8A87C, 0xC38D9E, 0x41B3A3]
vibrant_color_palette = [0xFC4445, 0x3FEEE6, 0x55BCC9, 0x97CAEF, 0xCAFAFE]
simple_color_palette = [0x0B0C10, 0x1F2833, 0xC5C6C7, 0x66FCF1, 0x45A29E]
clean_color_palette = [0x5680E9, 0x84CEEB, 0x5AB9EA, 0xC1C8E4, 0x8860D0]
accent_color_palette = [0x242582, 0x553D67, 0xF64C72, 0x99738E, 0x2F2FA2]
bold_color_palette = [0x1A1A1D, 0x4E4E50, 0x6F2232, 0x950740, 0xC3073F]
pastel_color_palette = [0xA1C3D1, 0xB39BC8, 0xF0EBF4, 0xF172A1, 0xE64398]


def random_color(ctx):
    authorid = str(ctx.author.id)
    with open("database/sodagame.json", "r") as f:
        data = json.load(f)
    try:
        data[authorid]["current colors"]
    except:
        return discord.Color.blue()
    if data[authorid]["current colors"] == "gsw colors":
        return random.choice(warriors_color_palette)
    elif data[authorid]["current colors"] == "balanced colors":
        return random.choice(balanced_color_palette)
    elif data[authorid]["current colors"] == "vibrant colors":
        return random.choice(vibrant_color_palette)
    elif data[authorid]["current colors"] == "simple colors":
        return random.choice(simple_color_palette)
    elif data[authorid]["current colors"] == "clean colors":
        return random.choice(clean_color_palette)
    elif data[authorid]["current colors"] == "accent colors":
        return random.choice(accent_color_palette)
    elif data[authorid]["current colors"] == "bold colors":
        return random.choice(bold_color_palette)
    elif data[authorid]["current colors"] == "pastel colors":
        return random.choice(pastel_color_palette)
    else:
        return random.choice(default_color_palette)


def bold(arg):
    return "**" + arg + "**"


def underline(arg):
    return "__" + arg + "__"


def in_jail(user_id):
    with open("database/jail.json", "r") as f:
        jail = json.load(f)
    return user_id in jail


def not_acc_exists(user_id):
    with open("database/sodagame.json", "r") as f:
        data = json.load(f)
    try:
        data[user_id]["wallet"]
        return False
    except:
        return True


def rand_cards(total, low=2, high=14):
    num = random.randint(low, high)
    strnum = str(num)
    if num == 11:
        strnum = "J"
        num = 10
    if num == 12:
        strnum = "Q"
        num = 10
    if num == 13:
        strnum = "K"
        num = 10
    if num == 14:
        num = 1 if total > 10 else 11
        strnum = "A"
    return [num, strnum]


def calc_perform_total(viewers, satisfaction):
    fan_gain = math.ceil((viewers * satisfaction / 100) * 0.8)
    payout = math.ceil(viewers * 15 * (satisfaction / 100))
    if viewers >= 1000:
        fan_gain = fan_gain * 0.75
        payout = payout * 0.75
    elif viewers >= 5000:
        fan_gain = fan_gain * 0.6
        payout = payout * 0.6
    elif viewers >= 10000:
        fan_gain = fan_gain * 0.5
        payout = payout * 0.5

    return [fan_gain, payout]


# async def update_bank(user_id, type = 0, amount = 0):


class SodaSelection(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, page):
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        with open("database/sodas.json", "r") as f:
            sodadata = json.load(f)
        # return discord.Embed(title="Title goes here", description = f"Page {menu.current_page+1}/{self.get_max_pages()}")
        offset = menu.current_page * self.per_page
        sodainv = data[str(menu.ctx.author.id)]["soda inventory"]
        em = discord.Embed(
            title=f"{sodadata[sodainv[offset]]['name']}",
            description=f"{sodadata[sodainv[offset]]['special effects']}",
            color=random_color(str(menu.ctx.author.id)),
        )
        em.set_footer(text=f"Page {menu.current_page+1}/{self.get_max_pages()}")
        try:
            sodas = SelectionButtons("hi").sodas
            sodas[str(menu.ctx.author.id)] = {}
            sodas[str(menu.ctx.author.id)]["sodas"] = [sodadata[sodainv[offset]]["name"]]
            sodas[str(menu.ctx.author.id)]["soda_id"] = str(int(sodainv[offset]))
            sodas[str(menu.ctx.author.id)]["in progress"] = "yes"
            # print(sodas)
        except:
            traceback.print_exc()
        return em


class SelectionButtons(menus.MenuPages):
    sodas = {}

    @menus.button("👍")
    async def select(self, payload):
        try:
            await self.message.delete()
            self.stop()
            p2 = SelectionSecondStep()
            await p2.start(self.ctx)
        except:
            traceback.print_exc()

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def end_menu(self, _):
        try:
            self.sodas[str(self.ctx.author.id)]["in progress"] = "no"
            self.stop()
            return await self.message.clear_reactions()
        except:
            traceback.print_exc()


class SelectionSecondStep(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        sodainv = data[str(self.ctx.author.id)]["soda inventory"]
        sodas = SelectionButtons("hi").sodas
        try:
            if sodainv.count(sodas[str(self.ctx.author.id)]["soda_id"]) > 1:
                await self.ctx.send(
                    f"You have more than 1 `{sodas[str(self.ctx.author.id)]['sodas'][0]}` in your inventory! If you select more than 1, you get a boost in fans and coins! How many `{sodas[str(self.ctx.author.id)]['sodas'][0]}s` do you want to select? (You currently have **{sodainv.count(sodas[str(self.ctx.author.id)]['soda_id'])}**)"
                )

                def check(m):
                    return m.channel == self.ctx.channel and m.author == self.ctx.author

                try:
                    res = await self.bot.wait_for("message", check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send("Didn't get an answer in time, aborting...")
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    return menus.Menu.stop(self)
                try:
                    res = int(res.content)
                except:
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    await self.ctx.send("Not a valid number! Aborting...")
                    return menus.Menu.stop(self)
                if res <= 0:
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    await self.ctx.send("You can't chug 0 or less sodas! That's kinda stupid ngl")
                    return menus.Menu.stop(self)
                if res <= sodainv.count(sodas[str(self.ctx.author.id)]["soda_id"]):
                    for i in range(res - 1):
                        sodas[str(self.ctx.author.id)]["sodas"].append(sodas[str(self.ctx.author.id)]["sodas"][0])
                else:
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    await self.ctx.send("You don't have that many! Aborting...")
                    return menus.Menu.stop(self)
        except:
            traceback.print_exc()
        # print(sodas[str(self.ctx.author.id)]['sodas'])
        em = discord.Embed(
            title="Confirmation",
            description=f"Are you sure you want to select this soda? `{len(sodas[str(self.ctx.author.id)]['sodas'])} {sodas[str(self.ctx.author.id)]['sodas'][0]}`",
            color=random_color(str(self.ctx.author.id)),
        )
        return await ctx.send(embed=em)

    @menus.button("✅")
    async def yes(self, payload):  # sourcery no-metrics
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        sodainv = data[str(self.ctx.author.id)]["soda inventory"]
        sodas = SelectionButtons("hi").sodas
        index = 0
        for item in sodainv:
            if item == sodas[str(self.ctx.author.id)]["soda_id"]:
                if len(data[str(self.ctx.author.id)]["soda inventory"]) == 1:
                    data[str(self.ctx.author.id)]["soda inventory"] = []
                else:
                    for x in range(len(sodas[str(self.ctx.author.id)]["sodas"])):
                        del data[str(self.ctx.author.id)]["soda inventory"][index]
                break
            index += 1
        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)
        await asyncio.sleep(1)
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        await self.message.edit(
            embed=discord.Embed(
                title="Success!",
                description=f"You have selected `{len(sodas[str(self.ctx.author.id)]['sodas'])} {sodas[str(self.ctx.author.id)]['sodas'][0]}` to be chugged.",
                color=random_color(str(self.ctx.author.id)),
            )
        )
        await self.message.clear_reactions()
        try:
            em = discord.Embed(
                title="Chugging Time!",
                description=f"{self.ctx.author.name} is performing at **{Game.perform.stadium}** for **{Game.perform.total_viewers}** viewers!",
                color=random_color(str(self.ctx.author.id)),
            )
            em.add_field(name="Current Soda", value=f"{sodas[str(self.ctx.author.id)]['sodas'][0]}")
            await self.ctx.send(embed=em)
            await asyncio.sleep(1)
            rand = random.randint(1, 3)
            if rand == 1:
                em1 = discord.Embed(
                    title="EZ Dubs!",
                    description="You chug everything with **EASE**! And just like that, you're finished! :clap:",
                    color=random_color(str(self.ctx.author.id)),
                )
                payout = calc_perform_total(Game.perform.total_viewers, random.randint(80, 100))[1]
                fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(80, 100))[0]
                em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                data[str(self.ctx.author.id)]["wallet"] += payout
                data[str(self.ctx.author.id)]["fans"] += fan_gain
                await asyncio.sleep(1)
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                await self.ctx.send(embed=em1)
                sodas[str(self.ctx.author.id)]["in progress"] = "no"
            elif rand == 2:
                em2 = discord.Embed(
                    title="Oh No!",
                    description="It's not looking good! You're getting nauseous, and it doesn't look like you'll be able to finish! There are only three possible choices: Stop, continue chugging, or do a funny dance and hope for the best. Quick! Make a decision! You can choose between `stop`, `continue`, and `funny dance`.",
                    color=discord.Color.green(),
                )
                await self.ctx.send(embed=em2)

                def check(m):
                    return m.channel == self.ctx.channel and m.author == self.ctx.author

                try:
                    res = await self.bot.wait_for("message", check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await self.ctx.send("You didn't respond in time!")
                    res = "stop"
                if res == "stop":
                    em1 = discord.Embed(
                        title="You stopped!",
                        description="You stare out at the crowd, to see looks of disappointment on their faces. But you know you made the right choice.",
                        color=random_color(str(self.ctx.author.id)),
                    )
                    payout = calc_perform_total(Game.perform.total_viewers, random.randint(60, 75))[1]
                    fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(60, 75))[0]
                    em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                    em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                    data[str(self.ctx.author.id)]["wallet"] += payout
                    data[str(self.ctx.author.id)]["fans"] += fan_gain
                    with open("database/sodagame.json", "w") as f:
                        data = json.dump(data, f, indent=4)
                    await self.ctx.send(embed=em1)
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                elif res.content.lower() == "continue":
                    rand1 = random.randint(1, 2)
                    if rand1 == 1:
                        fee = random.randint(50, 300)
                        networth = data[str(self.ctx.author.id)]["wallet"] + data[str(self.ctx.author.id)]["bank"]
                        fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(15, 40))[0]
                        payout = 0
                        if networth < fee:
                            em1 = discord.Embed(
                                title="Aw Man!",
                                description=f"So..... you fainted on the spot, and you were rushed to the hospital. You wake up to find that the hospital fee is <:badlands_coin:831628523180916736> {fee}. Unfortunately, your wallet PLUS bank amount was not even enough to pay off the expenses. You will be put in jail and prevented from doing any commands until someone bails you out by paying <:badlands_coin:831628523180916736> **100**. Hey, at least you got some new fans!",
                                color=discord.Color.red(),
                            )
                        else:
                            em1 = discord.Embed(
                                title="Aw Man!",
                                description=f"So..... you fainted on the spot, and you were rushed to the hospital. You wake up to find that the hospital fee is <:badlands_coin:831628523180916736> {fee}. You quickly hand over the money, annoyed by the fact that your chug was a failure. Thankfully, you still gained some fans! :)",
                                color=discord.Color.red(),
                            )
                            data[str(self.ctx.author.id)]["wallet"] -= fee
                            if data[str(self.ctx.author.id)]["wallet"] < 0:
                                recover_amount = data[str(self.ctx.author.id)]["wallet"] * -1
                                data[str(self.ctx.author.id)]["wallet"] += recover_amount
                                data[str(self.ctx.author.id)]["bank"] -= recover_amount
                            data[str(self.ctx.author.id)]["fans"] += fan_gain
                            await asyncio.sleep(1)
                            with open("database/sodagame.json", "w") as f:
                                data = json.dump(data, f, indent=4)
                        em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                        em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                        await self.ctx.send(embed=em1)
                        sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    else:
                        payout = calc_perform_total(Game.perform.total_viewers, random.randint(80, 100))[1]
                        fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(80, 100))[0]
                        em1 = discord.Embed(
                            title="Whew!",
                            description="You make it out alive! The crowd is very satisfied with your performance. Good job!",
                        )
                        em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                        em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                        data[str(self.ctx.author.id)]["wallet"] += payout
                        data[str(self.ctx.author.id)]["fans"] += fan_gain
                        with open("database/sodagame.json", "w") as f:
                            data = json.dump(data, f, indent=4)
                        await self.ctx.send(embed=em1)
                        sodas[str(self.ctx.author.id)]["in progress"] = "no"
                elif res.content.lower() == "funny dance":
                    rand4 = random.randint(1, 2)
                    if rand4 == 1:
                        payout = calc_perform_total(Game.perform.total_viewers, random.randint(5, 20))[1]
                        fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(5, 20))[0]
                        em1 = discord.Embed(
                            title="Bruh", description="The fans think you're an idiot. They are very disappointed."
                        )
                        em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                        em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                        data[str(self.ctx.author.id)]["wallet"] += payout
                        data[str(self.ctx.author.id)]["fans"] += fan_gain
                        with open("database/sodagame.json", "w") as f:
                            data = json.dump(data, f, indent=4)
                        await self.ctx.send(embed=em1)
                        sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    else:
                        payout = calc_perform_total(Game.perform.total_viewers, random.randint(70, 90))[1]
                        fan_gain = calc_perform_total(Game.perform.total_viewers, random.randint(70, 90))[0]
                        em1 = discord.Embed(
                            title="NICE!",
                            description="The crowd is amazed with your dance moves. You put on a **SHOW**! :fire: Great job!",
                        )
                        em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                        em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                        data[str(self.ctx.author.id)]["wallet"] += payout
                        data[str(self.ctx.author.id)]["fans"] += fan_gain
                        with open("database/sodagame.json", "w") as f:
                            data = json.dump(data, f, indent=4)
                        await self.ctx.send(embed=em1)
                        sodas[str(self.ctx.author.id)]["in progress"] = "no"
                else:
                    await self.ctx.send("That's not a valid choice!")
                    sodas[str(self.ctx.author.id)]["in progress"] = "no"
                    return

            else:
                dying_fails = [
                    "Someone poured a toxic substance into your drink! The moment your lips touched the drink, you were dead. You lose all of your wallet money, and gain NOTHING.",
                    "One of your enemies comes up to you with a hammer, and knocks you to death. Oof. You lose all of your wallet money.",
                    "Your get too nervous, and your heart disease kills you before the hospital even gets a chance at healing you.",
                ]
                normal_fails = [
                    "You aim at your nose instead of your mouth! When you notice, it's too late! You take a **huge** sneeze, and accidentally DROP the chug jug! :eyes: The crowd is very disappointed with your performance.",
                    "You forget to swallow, and ended up spitting out **ALL** of the soda at the fans! How rude! The fans are furious with your performance.",
                    "SHOOT! You chose a **WINE** instead of the soda you meant to choose! You're not used to drinking so much! You instantly stop, and apologize to the fans. The fans get very irritated and people start booing you. Poor you :)",
                    "You ate too much food before performing! You barf and all everything comes out. EWWWWW! The fans are very annoyed with you.",
                ]
                rand3 = random.randint(1, 3)
                if rand3 == 1:
                    description = random.choice(dying_fails)
                    data[str(self.ctx.author.id)]["wallet"] = 0
                else:
                    description = random.choice(normal_fails)
                em1 = discord.Embed(
                    title="EPIC Fail!", description=description, color=random_color(str(self.ctx.author.id))
                )
                payout = 0
                fan_gain = 0
                em1.add_field(name="Total Earnings", value=f"<:badlands_coin:831628523180916736> {payout}")
                em1.add_field(name="Fan Gain", value=f"You got **{fan_gain}** new fans!")
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                await self.ctx.send(embed=em1)
                sodas[str(self.ctx.author.id)]["in progress"] = "no"

        except:
            traceback.print_exc()

    @menus.button("❌")
    async def no(self, payload):
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        sodainv = data[str(self.ctx.author.id)]["soda inventory"]
        source = SodaSelection(range(1, len(sodainv) + 1))
        p = SelectionButtons(source)
        await self.message.delete()
        self.stop()
        return await p.start(self.ctx)


class Game(commands.Cog):
    """
    Chugs Royale is an amazing game about sodas that you should definitely try out!
    """

    def __init__(self, bot):
        self.bot = bot

    class SelectionMenu(menus.Menu):
        async def send_initial_message(self, ctx, channel):
            try:
                with open("database/sodagame.json", "r") as f:
                    data = json.load(f)
                sodainv = data[str(self.ctx.author.id)]["soda inventory"]
                source = SodaSelection(range(1, len(sodainv) + 1))
                p = SelectionButtons(source)
                return await p.start(self.ctx)
            except:
                traceback.print_exc()

    class Store(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=1)

        async def format_page(self, menu, entries):
            with open("database/store.json", "r") as f:
                store = json.load(f)
            offset = menu.current_page * self.per_page
            em = discord.Embed(
                title=f"{store[str(offset + 1)]['name']}",
                description=f"{store[str(offset + 1)]['description']}",
                color=random_color(str(menu.ctx.author.id)),
            )
            em.add_field(
                name="Price", value=f"Price: <:badlands_coin:831628523180916736> {store[str(offset + 1)]['price']}"
            )
            em.add_field(name="Buy Command", value=f"`?buy {store[str(offset + 1)]['nick']}`")
            em.set_footer(text=f"Page: {offset + 1}/{self.get_max_pages()}")
            return em

    async def calc_multi(self, user):
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        multi = data[user]["multi"]
        if user in ["681183140357865474", "792522702652702740"]:
            multi += 10

    @commands.command()
    async def start(self, ctx):
        """
        Starts the game, and gives you a mini tutorial!
        """
        user_id = str(ctx.author.id)
        em = discord.Embed(
            title="Welcome to Chugs Royale!",
            description="The **main** purpose of the game is to earn as many coins as possible. \nThe more coins you get, the better things you can buy.",
            color=random.choice(default_color_palette),
        )
        em.add_field(
            name="__SO HOW DO I GET COINS?__",
            value=":small_orange_diamond:  You can earn **COINS, XP, and FANS** by **chugging sodas**, which is basically the act of swallowing a beverage in a continuous action. **You do this in shows**, where you can gain coins and fans for **successful** chugs. To start a show, do `?peform`, and to check your balance, do `?bal`. To check any of your other stats, do `?profile`. You can also get coins by doing `?beg`, or `?search`.",
        )
        em.add_field(
            name="__WHERE DO I FIND DRINKS?__",
            value=":small_orange_diamond: You can find **drinks** by using the `?search` command. You will be provided with a list of 3 places to search, and you will choose between them. \n:small_orange_diamond: **Some drinks** will also be available in stores, and you can buy them with **coins**.",
            inline=False,
        )
        em.add_field(
            name="__OTHER FEATURES__",
            value=":small_orange_diamond: If you're lucky, you'll be provided with partnership oppurtunities **each time you do a command!** This will allow partnerships with **famous celebrities**, who will promote you and help you become **more famous**! \n:small_orange_diamond: The store won't just contain sodas, it may also contain XP boosters, and other fun but (possibly) useless items!",
            inline=False,
        )
        em.add_field(
            name="__ANY QUESTIONS?__",
            value=":small_orange_diamond: **DM Kool for help!** \n:small_orange_diamond: **Good luck!**",
            inline=False,
        )
        await ctx.send(embed=em)
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        with open("database/sodaeffects.json", "r") as f:
            data1 = json.load(f)
        try:
            data[user_id]
            data1[user_id]
        except:
            fmt = {
                "wallet": 0,
                "bank": 0,
                "xp": 0,
                "fans": 0,
                "multi": 0,
                "appeal": 0,
                "speed boost": 0,
                "soda inventory": [],
                "collectibles": [],
                "partnered celebrity": "",
                "current colors": "",
                "membership start dates": {"costco": ""},
            }
            fmt1 = {"caffeine": 0, "drunkness": 0, "fatigue": 0}

            data[user_id] = fmt
            data1[user_id] = fmt1
            with open("database/sodagame.json", "w") as f:
                data = json.dump(data, f, indent=4)
            with open("database/sodaeffects.json", "w") as f:
                data1 = json.dump(data1, f, indent=4)

    @commands.command(aliases=["prof", "p"])
    async def profile(self, ctx, user: discord.Member = None):
        """
        Check your profile and stats! (Fans, coins, etc.)
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        user = user or ctx.author

        user_id = str(user.id)

        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        with open("database/sodaeffects.json", "r") as f:
            data1 = json.load(f)

        wallet = data[user_id]["wallet"]
        bank = data[user_id]["bank"]
        xp = data[user_id]["xp"]
        fans = data[user_id]["fans"]
        sodacount = len(data[user_id]["soda inventory"])
        multi = data[user_id]["multi"]
        appeal = data[user_id]["appeal"]
        drunkness = data1[user_id]["drunkness"]
        caffeine = data1[user_id]["caffeine"]
        fatigue = data1[user_id]["fatigue"]
        speed = data[user_id]["speed boost"]

        if data[user_id]["partnered celebrity"] == "":
            partnerships = "No one at the moment"
        else:
            partnerships = data[user_id]["partnered celebrity"]

        em = discord.Embed(title=f"{user.name}'s Profile", color=random_color(str(ctx.author.id)))
        em.add_field(
            name="THE STACK",
            value=f":credit_card: **Credit Card**: {wallet} \n:bank: **Bank Locker**: {bank} \n:moneybag: **Net Worth**: {wallet + bank}",
        )
        em.add_field(name="THE FRIDGE", value=f":tropical_drink: **Drinks**: {sodacount}", inline=False)
        em.add_field(
            name="FANBASE", value=f":heart: **Fans**: {fans} \n:heartpulse: **Appeal**: {appeal}", inline=False
        )
        em.add_field(
            name="EFFECTS",
            value=f":beer: **Drunkness**: {drunkness}% \n:dizzy_face: **Fatigue**: {fatigue}% \n:coffee: **Caffeine**: {caffeine}% \n:arrow_right: **Speed**: {speed}",
            inline=False,
        )
        em.add_field(
            name="OTHER STATS",
            value=f":chart_with_upwards_trend: **XP**: {xp} \n:arrow_double_up: **Multiplier**: {multi}% \n:handshake: **Partnerships**: {partnerships}",
            inline=False,
        )
        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(text="Multipliers work on both your XP and Coins")
        await ctx.send(embed=em)

    @commands.command(name="effects", aliases=["ef"])
    async def effects(self, ctx):
        """
        Your drunk, caffeine, and fatigue levels.
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        user_id = str(ctx.author.id)
        with open("database/sodaeffects.json", "r") as f:
            data = json.load(f)
        try:
            drunkness = data[user_id]["drunkness"]
            caffeine = data[user_id]["caffeine"]
            fatigue = data[user_id]["fatigue"]
            drunkness = round(int(drunkness) / 10) * 10
            caffeine = round(int(caffeine) / 10) * 10
            fatigue = round(int(fatigue) / 10) * 10
            drunkbar = "".join(":blue_square:" for _ in range(int(drunkness / 10))) if drunkness != 0 else "None"
            caffeinebar = "".join(":green_square:" for _ in range(int(caffeine / 10))) if caffeine != 0 else "None"
            fatiguebar = "".join(":red_square:" for _ in range(int(fatigue / 10))) if fatigue != 0 else "None"
            em = discord.Embed(title=f"{ctx.author.name}'s Effects", color=random_color(str(ctx.author.id)))
            em.add_field(name="Drunkness", value=drunkbar, inline=False)
            em.add_field(name="Caffeine", value=caffeinebar, inline=False)
            em.add_field(name="Fatigue", value=fatiguebar, inline=False)
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(name="search")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def search(self, ctx):  # sourcery no-metrics
        """
        Search a store and get coins/sodas!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if in_jail(str(ctx.author.id)):
            return await ctx.send(
                "You're in jail! You can't use money-earning commands until you're bailed out by someone else."
            )
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        with open("database/sodas.json", "r") as f:
            data1 = json.load(f)
        user = ctx.author
        rand_money = random.randint(1, 100)
        sodalist = []
        sodaidlist = []
        for sodaid in data1:
            sodalist.append(data1[sodaid]["name"])
            sodaidlist.append(sodaid)
        soda = random.choice(sodalist)
        sodaid = sodaidlist[sodalist.index(soda)]
        fate = random.randint(1, 48)

        e = random.randint(1, 2)
        sodamsg = ""
        if e == 1:
            sodamsg = f"Lucky you! You additionally found 1 **{soda}**! Do you wish to buy it for <:badlands_coin:831628523180916736> **{math.ceil(data1[sodaid]['price']*0.8)}**? `(y/n)`"
        item_list = ["Walmart", "McDonalds", "Costco", "The Back Alley", "Specialty Soda Store", "711"]
        search_list = random.sample(item_list, 3)
        one, two, three = search_list
        await ctx.reply(
            f"**Where would you like to search? Please choose 1 of the following**:\n`{one}`, `{two}`, `{three}`"
        )

        for i in range(len(search_list)):
            search_list[i] = search_list[i].lower()

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            res = await self.bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("Can't search if you don't give me a place to. Sorry")
            return
        if res.content.lower() in search_list:
            if fate == 1:
                with open("database/jail.json", "r") as f:
                    jail = json.load(f)
                bail = random.randint(100, 1000)
                fmt = {"bail price": bail}
                jail[str(user.id)] = fmt
                with open("database/jail.json", "w") as f:
                    jail = json.dump(jail, f, indent=4)
                return await ctx.reply(
                    f"The police thought you were trying to rob the store, even though you're completely innocent. You go to jail without any trial, and the bail price is set at `{bail}`. Someone else will have to bail you out by using the command `?bail [ping you]`, and pay the bail price."
                )
            if fate == 2:
                data[str(user.id)]["wallet"] = 0
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                return await ctx.reply("You died and lost all of your wallet money. RIP :skull:")
            searchEmbed = discord.Embed(
                title="Searched: " + res.content.upper(),
                description=f"You found <:badlands_coin:831628523180916736> {rand_money}! {sodamsg}",
                color=random_color(str(ctx.author.id)),
            )
            data[str(user.id)]["wallet"] += int(rand_money)
            with open("database/sodagame.json", "w") as f:
                data = json.dump(data, f, indent=4)
            with open("database/sodagame.json", "r") as f:
                data = json.load(f)
            if sodamsg != "":
                searchEmbed.set_footer(text="The price of any soda you find in search is 80% of its store price.")
                searchEmbed.add_field(
                    name="Saved Amount",
                    value=f"Saved Amount: <:badlands_coin:831628523180916736> {data1[sodaid]['price'] - math.ceil(data1[sodaid]['price']*0.8)} \nStore Price: <:badlands_coin:831628523180916736> {data1[sodaid]['price']}",
                )
                searchEmbed.add_field(
                    name="Item Info",
                    value=f"Rarity: {data1[sodaid]['rarity'].title()} \nID: {sodaid} \nCaffeine: {data1[sodaid]['caffeine']}%",
                )
                if data[str(user.id)]["wallet"] >= data1[sodaid]["price"] * 0.8:
                    affordable = "Yes"
                else:
                    affordable = "No"
                searchEmbed.add_field(
                    name="Current Balance",
                    value=f"Wallet Balance: <:badlands_coin:831628523180916736> {data[str(user.id)]['wallet']} \nAffordable? **{affordable}** \nMoney After Purchase: <:badlands_coin:831628523180916736> {int(data[str(user.id)]['wallet'] - (data1[sodaid]['price'] * 0.8))}",
                )
            await ctx.reply(embed=searchEmbed)
            with open("database/sodagame.json", "w") as f:
                data = json.dump(data, f, indent=4)
            if e == 2:
                return
            try:
                res = await self.bot.wait_for("message", check=check, timeout=7.5)
            except asyncio.TimeoutError:
                await ctx.send("Didn't get a response in time, offer closed.")
                return
            if res.content.lower() == "y" or res.content.lower() == "yes":
                with open("database/sodagame.json", "r") as f:
                    data = json.load(f)
                if data[str(user.id)]["wallet"] < math.ceil(data1[sodaid]["price"] * 0.8):
                    await ctx.send(
                        "You don't have enough money on your credit card! Next time actually BRING some money out for shopping!"
                    )
                    return
                await ctx.send(
                    f"Nice, you bought 1 **{data1[sodaid]['name']}** for <:badlands_coin:831628523180916736> **{math.ceil(data1[sodaid]['price']*0.8)}**!"
                )
                data[str(user.id)]["soda inventory"].append(sodaid)
                try:
                    for soda in data[str(user.id)]["soda inventory"]:
                        soda = int(soda)
                    data[str(user.id)]["soda inventory"].sort(key=lambda x: int(x.split("-")[0]))
                    for soda in data[str(user.id)]["soda inventory"]:
                        soda = str(soda)
                except:
                    traceback.print_exc()
                data[str(user.id)]["wallet"] -= math.ceil(data1[sodaid]["price"] * 0.8)
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                return
            elif res.content.lower() == "n" or res.content.lower() == "no":
                await ctx.send("Ok, cancelling the offer...")
                return
            else:
                await ctx.send("That is not valid! You didn't get anything. Too bad")
                return
        else:
            await ctx.send("That is not valid! You didn't get anything. Too bad")

    @commands.command(aliases=["balance"])
    async def bal(self, ctx, user: discord.Member = None):
        """
        Check how many coins you have in your wallet and bank.
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        user = user or ctx.author
        user_id = str(user.id)
        try:
            with open("database/sodagame.json", "r") as f:
                data = json.load(f)
        except:
            traceback.print_exc()
        try:
            wallet = data[user_id]["wallet"]
            bank = data[user_id]["bank"]
            networth = wallet + bank
        except:
            await ctx.send("You don't have a profile right now! Do `?start` to get started!")
            return
        em = discord.Embed(
            title=f"{user.name}'s Stack",
            description=f":credit_card: **Wallet**: {wallet} \n:bank: **Bank**: {bank} \n:moneybag: **Net Worth**: {wallet + bank}",
            color=random_color(str(ctx.author.id)),
        )
        if networth <= 25000:
            em.set_footer(text="💩 Damn, you poor.")
        elif networth <= 100000:
            em.set_footer(text="Lower class peeps.")
        elif networth <= 250000:
            em.set_footer(text="Eh, I'd call that average.")
        elif networth <= 1000000:
            em.set_footer(text="Woooo! I see you earning that money! 👀")
        elif networth <= 2500000:
            em.set_footer(text="SHEESH! You rich! 💰")
        else:
            em.set_footer(text="Spoiled kid smh 🤑")
        await ctx.send(embed=em)

    @commands.command(name="bail")
    async def bail(self, ctx, user: discord.Member = None):
        """
        If someone is in jail, help them out by bailing them out!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if user == None:
            return await ctx.send("You can't bail out nobody!")
        if user == ctx.author:
            return await ctx.send("Haha I see you tryna bail yourself out, that is **__NOT ALLOWED__**")
        with open("database/jail.json", "r") as f:
            jail = json.load(f)
        with open("database/sodagame.json", "r") as f:
            userdata = json.load(f)
        if str(user.id) in jail:
            await ctx.send(
                f"Are you sure you want to bail out **{user.name}** for `{jail[str(user.id)]['bail price']}`? (`y/n`)"
            )

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            try:
                res = await self.bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send("Didn't get an answer in time, aborting...")
                return
            if res.content.lower() in ["y", "yes"]:
                if userdata[str(ctx.author.id)]["wallet"] >= jail[str(user.id)]["bail price"]:
                    userdata[str(ctx.author.id)]["wallet"] -= jail[str(user.id)]["bail price"]
                    del jail[str(user.id)]
                    with open("database/jail.json", "w") as f:
                        jail = json.dump(jail, f, indent=4)
                    with open("database/sodagame.json", "w") as f:
                        userdata = json.dump(userdata, f, indent=4)
                    await ctx.send(f"Successfully bailed out {user.name}!")
                else:
                    return await ctx.send(
                        f"You don't have enough money in your wallet! (You have **{coin} {userdata[str(ctx.author.id)]['wallet']}**)"
                    )
            else:
                return await ctx.send("Ok, aborting...")
        else:
            await ctx.send("That user is not in jail!")

    @commands.command(name="jail", aliases=["prison"])
    async def display_jail(self, ctx):
        """
        Want to check who's in jail, and who to bail out? Use this command!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        with open("database/jail.json", "r") as f:
            jail = json.load(f)
        description = (
            "".join(f"<@!{user}> - {coin} `{jail[user]['bail price']}`\n" for user in jail)
            if jail is not None
            else "This jail is currently empty"
        )

        await ctx.send(
            embed=discord.Embed(title="Arctic Jail", description=description, color=random_color(str(ctx.author.id)))
        )

    @commands.command(name="arrest")
    @commands.is_owner()  # Owner means owner of bot, not owner of server
    async def put_in_jail(self, ctx, user: discord.Member = None):
        """
        Owner-only, used to arrest certain people for being mean >:)
        """
        user = user or ctx.author
        with open("database/jail.json", "r") as f:
            jail = json.load(f)
        bail = random.randint(100, 1000)
        try:
            jail[str(user.id)]
        except:
            fmt = {"bail price": bail}
            jail[str(user.id)] = fmt
            with open("database/jail.json", "w") as f:
                jail = json.dump(jail, f, indent=4)
            return await ctx.send(f"Put {user.name} in jail for a bail price of `{bail}`!")
        await ctx.send("That user is already in jail!")

    @commands.command(name="free")
    @commands.is_owner()
    async def free_from_jail(self, ctx, user: discord.Member = None):
        """
        Owner-only, used rarely, as we can just use bail. Only difference is this command is free.
        """
        user = user or ctx.author
        with open("database/jail.json", "r") as f:
            jail = json.load(f)
        try:
            del jail[str(user.id)]
            with open("database/jail.json", "w") as f:
                jail = json.dump(jail, f, indent=4)
            return await ctx.send(
                f"Successfully freed {user.name} from jail! For free because you're the owner of the bot!"
            )
        except:
            await ctx.send("That user is not in jail!")

    @commands.command(name="beg")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def beg(self, ctx):  # sourcery no-metrics
        """
        Go around and beg for coins! A celebrity will notice you! There are some secret easter-eggs that give you even more coins! Try to figure them out!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if in_jail(str(ctx.author.id)):
            return await ctx.send(
                "You're in jail! You can't use money-earning commands until you're bailed out by someone else."
            )
        user = ctx.author
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        earnings = random.randint(1, 150)
        celebrities = [
            "Raspberry Pi",
            "Iann Dior",
            "Polo G",
            "Travis Scott",
            "Lil Uzi Vert",
            "Dream",
            "Prim",
            "Halsey",
            "Rosé (Blackpink)",
            "Whostolemyrice",
            "Ed Sheeran",
            "Jennie (Blackpink)",
            "Lisa (Blackpink)",
            "Cardi B",
            "Adam Levine",
            "Billie Eilish",
            "Demi Lovato",
            "The Weeknd",
            "Dua Lipa",
            "Brendon Urie",
            "Kelly Oubre Jr.",
            "Andrew Wiggins",
            "LeBron James",
            "Kevin Durant",
            "Damian Lillard",
            "Draymond Green",
            "Justin Bieber",
            "Stephen Curry",
            "Kool",
            "Olivia Rodrigo",
            "Juice WRLD",
            "Lil Mosey",
            "Post Malone",
            "Shawn Mendes",
            "Selena Gomez",
            "Klay Thompson",
            "Jisoo (Blackpink)",
            "Steve Kerr",
            "Technoblade",
            "Taylor Swift",
        ]
        num = random.randint(1, 100)
        if num == 5:
            earnings = 2000
            await ctx.reply(f"**OMG IT'S BADLANDS HIMSELF! HE GIVES YOU {coin} 2000!**")
        elif num == 6:
            earnings = 1
            await ctx.reply(f"**OMG IT'S MR. BEASTTTTTT! HE GIVES YOU {coin} 1!**")
        else:
            celebrity = random.choice(celebrities)
            user = ctx.author
            if user.activities:
                for activity in user.activities:
                    if isinstance(activity, Spotify) and celebrity.lower() in activity.artist.lower():
                        earnings = random.randint(250, 750)
            if (
                celebrity
                in [
                    "Stephen Curry",
                    "Kelly Oubre Jr.",
                    "Andrew Wiggins",
                    "Draymond Green",
                    "Klay Thompson",
                    "Steve Kerr",
                ]
                and data[str(user.id)]["current colors"] == "gsw colors"
            ):
                earnings = random.randint(250, 750)
            if data[str(user.id)]["wallet"] in [69, 420, 69420, 6969]:
                earnings = random.randint(250, 750)
            await ctx.reply(f"**{celebrity}** gave you {coin} **{earnings}**!")
        data[str(user.id)]["wallet"] += earnings
        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)

    @commands.command(name="fridge", aliases=["fri"])
    async def fridge(self, ctx):
        """
        Check what drinks you own, you can use these in ?perform
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        try:
            user_id = str(ctx.author.id)
            em = discord.Embed(title=f"{ctx.author.name}'s Fridge", color=random_color(str(ctx.author.id)))
            with open("database/sodagame.json", "r") as f:
                data = json.load(f)
            with open("database/sodas.json", "r") as f:
                data1 = json.load(f)
            fridge = data[user_id]["soda inventory"]
            countedsodas = []
            for soda in fridge:
                if soda not in countedsodas:
                    sodaname = data1[soda]["name"]
                    if fridge.count(soda) >= 2:
                        sodaname += f" X{fridge.count(soda)}"
                    sodadescription = data1[soda]["special effects"]
                    countedsodas.append(soda)
                    em.add_field(name=sodaname, value=sodadescription, inline=False)
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount=None):
        """
        Having all your money in your credit card is dangerous. If you die, you lose all your money there! Pesky robbers could steal your money! Therefore, you can deposit it into your bank, to be safe!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if in_jail(str(ctx.author.id)):
            return await ctx.send(
                "You're in jail! You can't use money-related commands until you're bailed out by someone else."
            )
        user_id = str(ctx.author.id)
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        try:
            data[user_id]["wallet"]
            data[user_id]["bank"]
        except:
            await ctx.send("You don't have a profile right now! Do `?start` to get started!")
            return

        if amount.lower() == "all":
            amount = data[user_id]["wallet"]

        amount = int(amount)

        if amount > data[user_id]["wallet"]:
            await ctx.send("That's more money than you have on your credit card!")
            return

        if amount < 0:
            await ctx.send("Bruh you can't deposit negative money")
            return

        data[user_id]["wallet"] -= amount
        data[user_id]["bank"] += amount

        try:
            await ctx.send(
                f"{ctx.author.mention} You deposited <:badlands_coin:831628523180916736> **{amount}**, current bank balance is <:badlands_coin:831628523180916736> **{data[user_id]['bank']}**"
            )
        except:
            traceback.print_exc()

        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)

    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount=None):
        """
        Withdraw money from your bank.
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if in_jail(str(ctx.author.id)):
            return await ctx.send(
                "You're in jail! You can't use money-related commands until you're bailed out by someone else."
            )
        user_id = str(ctx.author.id)
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        try:
            data[user_id]["wallet"]
            data[user_id]["bank"]
        except:
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")

        if amount.lower() == "all":
            amount = data[user_id]["bank"]

        amount = int(amount)

        if amount > data[user_id]["bank"]:
            await ctx.send("That's more money than you have in your bank!")
            return

        if amount < 0:
            await ctx.send("Bruh you can't withdraw negative money")
            return

        try:
            data[user_id]["wallet"] += amount
            data[user_id]["bank"] -= amount
        except:
            traceback.print_exc()

        try:
            await ctx.send(
                f"{ctx.author.mention} You withdrew <:badlands_coin:831628523180916736> **{amount}**, current bank balance is <:badlands_coin:831628523180916736> **{data[user_id]['bank']}**"
            )
        except:
            traceback.print_exc()

        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)

    @commands.command(name="give", aliases=["send"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def give(self, ctx, user: discord.Member = None, amount=None):
        """
        Want to give money to your friends? You can use this command!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if user == None:
            return await ctx.send("You didn't provide a valid user")
        if user == ctx.author:
            return await ctx.send("Why tf are you sending money to yourself, that's stupid asf.")
        if amount == None:
            return await ctx.send("You didn't provide a valid amount bruh")
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        if amount.lower() == "all":
            amount = data[str(ctx.author.id)]["wallet"]
        amount = int(amount)
        if amount <= 0:
            return await ctx.send("How do you send 0 or less coins that makes no sense at all")
        if amount > data[str(ctx.author.id)]["wallet"]:
            return await ctx.send("You don't even have that much wtf")
        data[str(ctx.author.id)]["wallet"] -= amount
        data[str(user.id)]["wallet"] += amount
        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)
        await ctx.reply(f"Success! You gave **{user.name}** {coin} **{amount}**!")

    @commands.command(name="rob", aliases=["steal"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member = None):
        """
        Want to gain more money? You can ROB people! You will get a random amount of money from the person you rob's wallet. Small chance they could end up robbing you tho...
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if user == None:
            return await ctx.send("HAHA TRYNA ROB NO ONE LMFAOOOOOO")
        if user == ctx.author:
            return await ctx.send("Dontcha think it's kinda stupid to rob yourself...?")
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        if data[str(user.id)]["wallet"] < 250:
            return await ctx.send("It's not worth it! They have less than 250 coins!")
        if data[str(ctx.author.id)]["wallet"] < 250:
            return await ctx.send(
                "Sorry, but you'll need at least 250 coins in your wallet whenever you go out for a robbery."
            )
        money_loss = random.randint(1, data[str(user.id)]["wallet"])
        success = random.randint(1, 5)
        if success != 1:
            await ctx.reply(f"Niceeeeeee! You stole {coin} **{money_loss}** from **{user.name}**!")
            data[str(ctx.author.id)]["wallet"] += money_loss
            data[str(user.id)]["wallet"] -= money_loss
        else:
            await ctx.reply(f"HAHAHA, {user.name} ended up robbing YOU and got 250 coins!")
            data[str(ctx.author.id)]["wallet"] -= 250
            data[str(user.id)]["wallet"] += 250
        with open("database/sodagame.json", "w") as f:
            data = json.dump(data, f, indent=4)

    @commands.command(aliases=["perf"])
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def perform(self, ctx):
        """
        The biggest coin-earning command at the moment, you can chug sodas in front of huge crowds! You need at least 2 sodas to do this. Use ?search to find some!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if in_jail(str(ctx.author.id)):
            return await ctx.send(
                "You're in jail! You can't use money-earning commands until you're bailed out by someone else."
            )
        try:
            sodas = SelectionButtons("hi").sodas
            if sodas[str(ctx.author.id)]["in progress"] == "yes":
                ctx.command.reset_cooldown(ctx)
                return await ctx.send("You already have a performance in progress!")
        except:
            pass
            # traceback.print_exc()
        with open("database/sodagame.json", "r") as f:
            userdata = json.load(f)
        sodainv = userdata[str(ctx.author.id)]["soda inventory"]
        if sodainv == []:
            em = discord.Embed(
                title="No Sodas!",
                description="You don't have any sodas in your inventory! Do `?search` to find some!",
                color=random_color(str(ctx.author.id)),
            )
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=em)
        if len(sodainv) == 1:
            em = discord.Embed(
                title="Not Enough Sodas!",
                description="You need at least **2** sodas in your inventory to perform! Do `?search` to find some!",
                color=random_color(str(ctx.author.id)),
            )
            return await ctx.send(embed=em)
        total_viewers = random.randint(
            math.ceil((userdata[str(ctx.author.id)]["fans"] + 20) * 0.25),
            math.ceil((userdata[str(ctx.author.id)]["fans"] + 20) * 2.5),
        )
        stadiums = [
            "Chase Center",
            "MetLife Stadium",
            "Philips Arena",
            "Staples Center",
            "Madison Square Garden",
            "Carnegie Hall",
            "Sydney Opera House",
        ]
        stadium = random.choice(stadiums)
        em = discord.Embed(
            title=f"{ctx.author.name} is Performing!",
            description=f"**{total_viewers} viewers** have gathered at {stadium} to watch you chug sodas!",
            color=random_color(str(ctx.author.id)),
        )
        em.add_field(name=":heartpulse: Current Appeal Level", value=userdata[str(ctx.author.id)]["appeal"])
        em.add_field(name=":arrow_double_up: Multiplier", value=f"{userdata[str(ctx.author.id)]['multi']}%")
        em.set_footer(text="You can do it!")
        await ctx.send(embed=em)
        try:
            Game.perform.stadium = stadium
            Game.perform.total_viewers = total_viewers
        except:
            pass
            # traceback.print_exc()
        await asyncio.sleep(1)
        str(ctx.author.id)
        test = self.SelectionMenu()
        await test.start(ctx)

    @commands.command()
    @commands.is_owner()
    async def blackjack(self, ctx):  # sourcery no-metrics
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        try:
            if bj_userinfo[str(ctx.author.id)]["gamegoing"] == True:
                return await ctx.send("You already have a game going!")
        except:
            pass
        try:

            fmt = {"gamegoing": True, "result": ""}
            bj_userinfo[str(ctx.author.id)] = fmt

            content = "What do you do? \nType `h` to hit, `s` to stand, and `e` to end the game."
            royals = {"A": [11, 1], "J": 11, "Q": 12, "K": 13}
            suits = ["♠︎", "♥", "♣", "♦"]
            user1 = rand_cards(0)
            user2 = rand_cards(0)
            user1_str = user1[1]
            user2_str = user2[1]
            usertotal = user1[0] + user2[0]
            if usertotal >= 21:
                while usertotal >= 21:
                    user1 = rand_cards(0)
                    user2 = rand_cards(0)
                    user1_str = user1[1]
                    user2_str = user2[1]
                    usertotal = user1[0] + user2[0]
            bot = rand_cards(0)
            bot_str = bot[1]
            bottotal = bot[0]
            em = discord.Embed()
            em.add_field(
                name=ctx.author.name,
                value=f"Cards - [`{random.choice(suits)} {user1_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) [`{random.choice(suits)} {user2_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) \nTotal - `{usertotal}`",
            )
            em.add_field(
                name="Penguin",
                value=f"Cards - [`{random.choice(suits)} {bot_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `?` \nTotal - `?`",
            )
            em.set_author(
                name=f"{ctx.message.author.name}'s Blackjack Game", icon_url=str(ctx.message.author.avatar_url)
            )
            await ctx.send(content=content, embed=em)
            fmt = {"i": 0}
            fmt2 = {"s": 0}
            bj_userinfo[str(ctx.author.id)].update(fmt)
            bj_userinfo[str(ctx.author.id)].update(fmt2)
            bot_cards = f"Cards - [`{random.choice(suits)} {bot_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `?` \nTotal - `?`"
            while bj_userinfo[str(ctx.author.id)]["gamegoing"] == True:

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                try:
                    res = await self.bot.wait_for("message", check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send(
                        "Bruhhhhhh I've been waiting for hours for an answer already. You lose all of the amount you bet."
                    )
                    return
                if res.content.lower() in ["h", "hit"]:
                    bj_userinfo[str(ctx.author.id)]["i"] += 1
                    i = bj_userinfo[str(ctx.author.id)]["i"]
                    added = rand_cards(usertotal, 2, 10)
                    usernew_str = added[1]
                    usernew = added[0]
                    usertotal += usernew

                    if usertotal > 21:
                        bj_userinfo[str(ctx.author.id)]["gamegoing"] = False
                        bj_userinfo[str(ctx.author.id)]["result"] = "lose"
                        content = "You busted! You lose..."
                        # await ctx.send("You lost!")
                    elif usertotal == 21:
                        bj_userinfo[str(ctx.author.id)]["gamegoing"] = False
                        bj_userinfo[str(ctx.author.id)]["result"] = "win"
                        content = "You reached 21 before Penguin! You win!"
                        # await ctx.send("You won!")
                    else:
                        pass
                    fmt = {str(i): usernew_str}
                    bj_userinfo[str(ctx.author.id)].update(fmt)
                elif res.content.lower() in ["s", "stand"]:
                    if bj_userinfo[str(ctx.author.id)]["s"] == 0:
                        bot_cards = (
                            f"Cards - [`{random.choice(suits)} {bot_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
                        )
                    bj_userinfo[str(ctx.author.id)]["s"] += 1
                    while bj_userinfo[str(ctx.author.id)]["result"] == "":
                        bot_new = rand_cards(bottotal)
                        bot_int = bot_new[0]
                        bot_string = bot_new[1]
                        bot_cards += (
                            f" [`{random.choice(suits)} {bot_string}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
                        )
                        bottotal += bot_int
                        if bottotal > 21:
                            bj_userinfo[str(ctx.author.id)]["gamegoing"] = False
                            bj_userinfo[str(ctx.author.id)]["result"] = "win"
                            content = "Penguin busted! You win!"
                        elif bottotal == 21:
                            bj_userinfo[str(ctx.author.id)]["gamegoing"] = False
                            bj_userinfo[str(ctx.author.id)]["result"] = "lose"
                            content = "Penguin reached 21 before you! You lose..."
                        elif bottotal > usertotal:
                            bj_userinfo[str(ctx.author.id)]["gamegoing"] = False
                            bj_userinfo[str(ctx.author.id)]["result"] = "lose"
                            content = f"You lose, Penguin has {bottotal}, you have {usertotal}."
                    bot_cards += f"\nTotal: `{bottotal}`"
                else:
                    pass
                color = 0x000000
                if bj_userinfo[str(ctx.author.id)]["result"] == "win":
                    color = discord.Color.green()

                if bj_userinfo[str(ctx.author.id)]["result"] == "lose":
                    color = discord.Color.red()
                content = bold(content)
                em = discord.Embed(color=color)
                user_cards = f"[`{random.choice(suits)} {user1_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ) [`{random.choice(suits)} {user2_str}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
                i = bj_userinfo[str(ctx.author.id)]["i"]
                for x in range(i):
                    y = x + 1
                    user_cards += f" [`{random.choice(suits)} {bj_userinfo[str(ctx.author.id)][str(y)]}`](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
                em.add_field(name=ctx.author.name, value=f"Cards - {user_cards} \nTotal - `{usertotal}`")
                em.add_field(name="Penguin", value=bot_cards)
                em.set_author(
                    name=f"{ctx.message.author.name}'s Blackjack Game", icon_url=str(ctx.message.author.avatar_url)
                )
                await ctx.send(content=content, embed=em)
        except:
            traceback.print_exc()

    @commands.command(aliases=["slot"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slots(self, ctx, amount=None):  # sourcery no-metrics
        """
        Gamble your money with slots! Need at least 2 of the same emoji to win, otherwise you lose your bet amount.
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)

        user_id = str(ctx.author.id)

        if amount is None:
            return await ctx.send("You need an amount smh -.-")
        if amount.lower() == "all":
            amount = data[user_id]["wallet"]
            amount = int(amount)

        amount = int(amount)

        if amount > data[user_id]["wallet"]:
            await ctx.send("Not enough money in your wallet.")
            return
        if amount < 0:
            await ctx.send("Amount has to be positive.")
            return
        if amount < 50:
            await ctx.send("Amount must be greater than or equal to 50.")
            return

        final = []

        for _ in range(3):
            a = random.choice(
                [
                    ":tropical_drink:",
                    ":champagne:",
                    ":cup_with_straw:",
                    ":tumbler_glass:",
                    ":bubble_tea:",
                    ":beverage_box:",
                    ":beer:",
                    ":wine_glass:",
                    ":milk:",
                    ":tea:",
                    ":coffee:",
                ]
            )
            final.append(a)
        s = " | "
        s = s.join(final)

        em = discord.Embed(title="Slots Results", description=f"**<**{s}**>**")
        msg = await ctx.send(embed=em)
        await asyncio.sleep(1)

        if final[0] == final[1] == final[2]:
            winnings = amount * 2
            em2 = discord.Embed(
                title="Slots Results",
                description=f"**<**{s}**>** \n \n JACKPOT! You get {winnings} coins.",
                color=discord.Color(0x00FF00),
            )
            await msg.edit(embed=em2)
            if final[0] == ":bubble_tea:":
                winnings = amount * 6
                em2 = discord.Embed(
                    title="Slots Results",
                    description=f"**<**{s}**>** \n \n **MEGA JACKPOT!** You get {winnings} coins.",
                    color=discord.Color(0x00FF00),
                )
                await msg.edit(embed=em2)
                data[user_id]["wallet"] += winnings
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                return
        elif final[0] == final[1] or final[0] == final[2] or final[1] == final[2]:
            winnings = amount
            em2 = discord.Embed(
                title="Slots Results",
                description=f"**<**{s}**>** \n \n You won! You get {winnings} coins.",
                color=discord.Color(0x00FF00),
            )
            await msg.edit(embed=em2)
            data[user_id]["wallet"] += winnings
            with open("database/sodagame.json", "w") as f:
                data = json.dump(data, f, indent=4)
        else:
            if final[0] == ":bubble_tea:" or final[1] == ":bubble_tea:" or final[2] == ":bubble_tea:":
                await ctx.send("The **boba tea** saved you! You don't gain or lose any money.")
            else:
                em2 = discord.Embed(
                    title="Slots Results",
                    description=f"**<**{s}**>** \n \n Unfortunate. You lost. You lose {amount} coins.",
                    color=discord.Color(0xFF0000),
                )
                await msg.edit(embed=em2)
                data[user_id]["wallet"] -= amount
                with open("database/sodagame.json", "w") as f:
                    data = json.dump(data, f, indent=4)

    @commands.group(name="store", aliases=["shop"])
    async def store(self, ctx):
        if ctx.invoked_subcommand is None:
            """
            Check out our store, where you can buy color schemes, special memberships, sodas, collectibles to flex, and much more!
            """
            if not_acc_exists(str(ctx.author.id)):
                return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
            with open("database/store.json", "r") as f:
                storedata = json.load(f)
            store = menus.MenuPages(source=self.Store(range(1, len(storedata) + 1)), clear_reactions_after=True)
            await store.start(ctx)

    @store.command(name="soda", aliases=["sodas"])
    async def store_soads(self, ctx, page=1):
        try:
            with open("database/sodas.json", "r") as f:
                sodas = json.load(f)
            page = int(page)
            pages = math.ceil(len(sodas) / 10)
            if page > pages:
                return await ctx.send("There aren't that many pages!")
            em = discord.Embed(
                title="Soda Store", description="Buy sodas here!", color=random_color(str(ctx.author.id))
            )
            items_desc = ""
            count = 0
            for soda in sodas:
                if count == 10:
                    break
                if list(sodas.keys()).index(soda) < (page - 1) * 10:
                    continue
                items_desc += (
                    f"**{sodas[soda]['name']}—{coin} {sodas[soda]['price']}** \n {sodas[soda]['special effects']} \n\n"
                )
                count += 1
            em.add_field(name="Sodas", value=items_desc)
            em.set_footer(text=f"Page: {page}/{pages}")
            await ctx.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command(name="buy", aliases=["purchase"])
    async def buy(self, ctx, *, arg):
        """
        Use this to buy something from the store.
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        with open("database/store.json", "r") as f:
            storedata = json.load(f)
        with open("database/sodagame.json", "r") as f:
            userdata = json.load(f)
        founditem = False
        itemid = ""
        for item_id in storedata:
            if arg.lower() == storedata[item_id]["nick"]:
                founditem = True
                itemid = item_id
                break
        if founditem == False:
            await ctx.send("Could not find that item in store!")
        else:
            if storedata[itemid]["price"] > userdata[str(ctx.author.id)]["wallet"]:
                await ctx.reply("You can't afford that item! Make sure you have enough money on your **Credit Card**.")
                return
            if itemid in userdata[str(ctx.author.id)]["collectibles"]:
                await ctx.reply("You already have that item!")
                return
            em = discord.Embed(
                title=f"{ctx.author.name} Just Purchased {storedata[itemid]['name']}!",
                description="Some data about the item will shown below.",
                color=random_color(str(ctx.author.id)),
            )
            em.add_field(name="Name of Item", value=storedata[itemid]["name"])
            em.add_field(name="Description", value=storedata[itemid]["description"], inline=False)
            em.add_field(name="Item Nickname", value=storedata[itemid]["nick"], inline=False)
            em.add_field(name="Item ID", value=itemid, inline=False)
            em.add_field(name="Item Type", value=storedata[itemid]["type"].title(), inline=False)
            userdata[str(ctx.author.id)]["collectibles"].append(itemid)
            userdata[str(ctx.author.id)]["wallet"] -= storedata[itemid]["price"]
            with open("database/sodagame.json", "w") as f:
                userdata = json.dump(userdata, f, indent=4)
            await ctx.reply(embed=em)

    @commands.group(name="colors", aliases=["scheme", "color"])
    async def colors(self, ctx):
        """
        Check out your color schemes! If you don't have any, you can buy some from store!
        """
        if not_acc_exists(str(ctx.author.id)):
            return await ctx.send("You don't have a profile right now! Do `?start` to get started!")
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid subcommand! For example, `?colors list`, `?colors select 1`.")

    @colors.command(name="list", aliases=["show"])
    async def colors_list(self, ctx):
        with open("database/sodagame.json", "r") as f:
            userdata = json.load(f)
        with open("database/store.json", "r") as f:
            store = json.load(f)
        user_id = str(ctx.author.id)
        inventory = userdata[user_id]["collectibles"]
        color_list = []
        color_list_nicks = []
        for item in inventory:
            if store[item]["type"] == "colors":
                color_list.append(store[item]["name"])
                color_list_nicks.append(store[item]["nick"])
        description = ""
        selected = userdata[user_id]["current colors"]
        for color in color_list:
            if color_list_nicks[color_list.index(color)] == selected:
                description += bold(f"{color_list.index(color) + 1}. {color} - Selected")
            else:
                description += f"{color_list.index(color) + 1}. {color}"
            if color_list.index(color) != len(color_list) - 1:
                description += "\n\n"
        if description == "":
            description = "You don't any color schemes other than the default! Find some to buy in store! `?store`"
        em = discord.Embed(
            title=f"{ctx.author.name}'s Color Schemes", description=description, color=random_color(user_id)
        )
        em.set_footer(text=f"Total Owned: {len(color_list)}")
        await ctx.send(embed=em)

    @colors.command(name="select", aliases=["choose", "set", "change", "switch"])
    async def select(self, ctx, arg):
        with open("database/sodagame.json", "r") as f:
            userdata = json.load(f)
        with open("database/store.json", "r") as f:
            store = json.load(f)
        og_color = userdata[str(ctx.author.id)]["current colors"]
        if arg in ["d", "default", "0"]:
            userdata[str(ctx.author.id)]["current colors"] = ""
            with open("database/sodagame.json", "w") as f:
                userdata = json.dump(userdata, f, indent=4)
            await ctx.send(f"Success! You have replaced `{og_color}` with `default` as your current color scheme!")
            return
        try:
            index = int(arg)
        except:
            await ctx.send("Please send a valid index! E.g. `?colors select 1`")
            return
        user_id = str(ctx.author.id)
        inventory = userdata[user_id]["collectibles"]
        color_list = []
        for item in inventory:
            if store[item]["type"] == "colors":
                color_list.append(store[item]["nick"])
        if og_color == "":
            og_color = "Default Colors"
        if color_list[index - 1] == og_color:
            return await ctx.send(f"You already have `{color_list[index-1]}` as your selected color scheme!")

        try:
            userdata[str(ctx.author.id)]["current colors"] = color_list[index - 1]
            with open("database/sodagame.json", "w") as f:
                userdata = json.dump(userdata, f, indent=4)
        except:
            await ctx.send("You don't own that color!")
            return
        await ctx.send(
            f"Success! You have replaced `{og_color}` with `{color_list[index-1]}` as your current color scheme!"
        )

    @commands.command()
    async def coke(self, ctx):
        try:
            embed = discord.Embed(title="Title", description="Desc", color=0x00FF00)  # creates embed
            file = discord.File("Images/Fanta_Shokata.png", filename="Fanta_Shokata.png")
            embed.set_thumbnail(url="attachment://Fanta_Shokata.png")
            await ctx.send(file=file, embed=embed)
        except:
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def updatesodaeffects(self, ctx):
        """
        Owner-only, utility command for the database.
        """
        with open("database/sodaeffects.json", "r") as f:
            data = json.load(f)

        fmt = {"caffeine": 0, "drunkness": 0, "fatigue": 0}

        with open("database/sodagame.json", "r") as f:
            data1 = json.load(f)

        for user_id in data1:
            try:
                data[user_id]
            except:
                data[user_id] = {}
                data[user_id].update(fmt)

        with open("database/sodaeffects.json", "w") as f:
            data = json.dump(data, f, indent=4)

        await ctx.send("Success.")

    # @commands.command(aliases=['drink'])
    # async def chug(self, ctx):
    #   try:
    #     user_id = str(ctx.author.id)
    #     em = discord.Embed(title = f"What do you want to chug?", color = random_color(str(ctx.author.id)))
    #     with open("database/sodagame.json", "r") as f:
    #       data = json.load(f)
    #     with open("database/sodas.json", "r") as f:
    #       data1 = json.load(f)
    #     fridge = data[user_id]["soda inventory"]
    #     fridge.sort()
    #     fridge = list(set(fridge))
    #     drinkList = [data1[x] for x in fridge if x >0]

    #   except:
    #     traceback.print_exc()


def setup(bot):
    bot.add_cog(Game(bot))
