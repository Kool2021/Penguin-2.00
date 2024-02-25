import asyncio
import json
import random
import traceback

from typing import Optional

import discord


import matplotlib.pyplot as plt
from discord import TextChannel
from discord.ext import commands


from prsaw import RandomStuff


def random_color():
    return random.randint(0, 0xFFFFFF)


api_key = "Your API Key"
rs = RandomStuff(api_key="uqTiluNPr8S5")


class Staff(commands.Cog):
    """
    Staff only :smirk:
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user: discord.Member, *, message: str):
        """
        DMs a user the following message
        """
        await user.send(message)
        await ctx.send(f"DMed {user} the following message: `{message}`")

    @commands.command()
    async def staffgraph(self, ctx, *, arg=None):
        """
        Displays a bar graph containing each staff member and the specified category. Try **?staffgraph messages**.
        """
        if arg == None:
            await ctx.send("Please provide a specific category. For example, `?staffgraph messages`")
            return

        with open("database/staffdata.json", "r") as f:
            data = json.load(f)

        try:
            data["541482948155670548"][arg]
        except:
            await ctx.send("Invalid. Try `?staffgraph messages`")
            return

        # group_data = list(data.values())
        group_data = []
        group_names = []
        total = 0
        async with ctx.typing():
            for user_id in data:
                group_data.append(data[user_id][arg])
                total += data[user_id][arg]
                user_id = int(user_id)
                username = await self.bot.fetch_user(user_id)
                group_names.append(username.name)
                group_data_sorted = sorted(group_data, reverse=True)
                # group_names = list(data.keys())
                # group_mean = np.mean(group_data)
            fig, ax = plt.subplots()
            plt.title(f"Staff Leaderboard for {arg.capitalize()}", fontsize=30)
            ax.barh(group_names, group_data)
            fig.set_size_inches(15.5, 12.5, forward=True)
            ax.set_facecolor("#c6e6fb")
            plt.savefig("staffgraph.png")
            file = discord.File("staffgraph.png")
            # data_stream = io.BytesIO()
            # data_stream.seek(0)
            # chart = discord.File(fp = "staffgraph.png",filename="staphgraph.png")
            em = discord.Embed(
                title=f"Staff {arg.capitalize()} Bar Graph",
                description=f"**Staff Total:** `{total}`",
                color=discord.Color.green(),
            )
            em.add_field(name="First :first_place:", value=f"`{group_data_sorted[0]}`")
            em.add_field(name="Second :second_place:", value=f"`{group_data_sorted[1]}`")
            em.add_field(name="Third :third_place:", value=f"`{group_data_sorted[2]}`")
            em.set_image(url="attachment://staffgraph.png")
            em.set_footer(text="Damnnnnn such a great staff team ngl")
            await ctx.send(embed=em, file=file)
        # plt.show()

    @commands.command()
    async def test(self, ctx, *, arg):
        """
        When you think the bot is down, try **?test [write anything here]**. If the bot is on and working, it will echo what you write
        """
        await ctx.send(arg)

    # @commands.group(name = 'reqs')
    # async def reqs(self, ctx):
    #   if ctx.invoked_subcommand is None:
    #     await ctx.send("Please provide a subcommand. An example would be `?reqs data`.")

    # @reqs.command(name = 'data')
    # async def req_data(self, ctx):
    #   await ctx.send("Nice reqs")

    @commands.command()
    async def stafflist(self, ctx):
        """
        Displays a list of all staff members
        """
        member = ctx.author
        em = discord.Embed(title="The Arctic Server's Staff Members", color=discord.Color.green())
        helper_role = discord.utils.get(member.guild.roles, id=797576724442513482)
        mod_role = discord.utils.get(member.guild.roles, id=797255250922045441)
        admin_role = discord.utils.get(member.guild.roles, id=822263561039904798)
        helpers = [m.name for m in helper_role.members]
        mods = [m.name for m in mod_role.members]
        admins = [m.name for m in admin_role.members]
        helpers_list = ""
        mods_list = ""
        admins_list = ""
        for helper in helpers:
            helpers_list += f"{helper}\n"
        for mod in mods:
            mods_list += f"{mod}\n"
        for admin in admins:
            admins_list += f"{admin}\n"

        em.add_field(name="Admins", value=admins_list, inline=False)
        em.add_field(name="Moderators", value=mods_list, inline=False)
        em.add_field(name="Helpers", value=helpers_list, inline=False)
        em.set_footer(text="Note: This excludes trial staff")

        await ctx.send(embed=em)

    @commands.command(name="deleterole", aliases=["delrole", "roledel", "roledelete", "drole"])
    @commands.is_owner()
    async def delrole(self, ctx, role: discord.Role = None):
        """
        Deletes the specified role
        """
        if role == None:
            return await ctx.send("You need to specify a role!")
        try:
            await role.delete()
            await ctx.send("The role `{}` has been deleted!".format(role.name))
        except:
            traceback.print_exc()

    @commands.command(name="createrole", aliases=["makerole", "addrole", "roleadd", "ar"])
    @commands.is_owner()
    async def addrole(self, ctx, color: discord.Color, *, name="new role"):
        """Creates a new role. Example would be **?createrole 123456 New Random Role**."""
        try:
            guild = ctx.guild
            newrole = await guild.create_role(name=name, color=color)
            await ctx.send(f"Created the role {newrole.mention}")
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="There Was An Error",
                    description="Make sure to use the correct format: `?createrole [hex for color] [name]`. An example would be `?createrole 000001 New Role`",
                    color=discord.Color.red(),
                )
            )

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def cnick(self, ctx, member: discord.Member = None, *, nick):
        """
        Changes the nickname of a member. Must have the manage nicknames permission.
        """
        try:
            member = ctx.author if not member else member
            await member.edit(nick=nick)
            await ctx.channel.send(f"{member.name}'s nickname was changed to `{nick}`")
        except:
            traceback.print_exc()

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def resetnick(self, ctx, member: discord.Member = None):
        """Resets the nickname of a specified member. Must have the manage nicknames permission."""
        member = ctx.author if not member else member
        await member.edit(nick=None)
        await ctx.send(f"Reset nickname for {member.name}")

    @commands.command()
    async def reqdata(self, ctx):
        """For staff members, to check your progress of your own staff reqs"""
        member = ctx.author
        role = discord.utils.get(member.guild.roles, id=797290799083683902)
        staff = [m.name for m in role.members]
        if str(member.name) in staff:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)

            # print(member.name)
            staffid = str(member.id)
            # print(staffid)

            gawpoints = data[staffid]["gawpoints"]
            events = data[staffid]["events"]
            invites = data[staffid]["invites"]
            messages = data[staffid]["messages"]
            genmessages = data[staffid]["genmessages"]
            # tallies = data[staffid]["tallies"]
            # print("Data received.")
            if genmessages >= 150 or gawpoints >= 3 or events >= 1 or invites >= 1 or messages >= 500:
                msg1 = "You are done for the day!"
                msg2 = "DM Kool to get your tally."
            else:
                msg1 = "You are not done for the day."
                msg2 = "Oof."

            em = discord.Embed(
                title=f"{member.name}'s Staff Reqs",
                description=f"**Giveaway Points:** {data[staffid]['gawpoints']} \n\n **Events:** {data[staffid]['events']} \n\n **Invites:** {data[staffid]['invites']} \n\n **Total Messages:** {data[staffid]['messages']} \n\n **General Messages:** {data[staffid]['genmessages']}",
                color=random_color(),
            )
            em.set_footer(text=f"{msg1} {msg2}")
            await ctx.send(embed=em)
        else:
            await ctx.send("You are not staff lol")

    @commands.command()
    @commands.is_owner()
    async def ownerreqdata(self, ctx, member: discord.Member):
        """Owner-only, to check on other staff member's req data."""
        role = discord.utils.get(member.guild.roles, id=797290799083683902)
        staff = [m.name for m in role.members]
        if str(member.name) in staff:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)

            # print(member.name)
            staffid = str(member.id)
            # print(staffid)

            gawpoints = data[staffid]["gawpoints"]
            events = data[staffid]["events"]
            invites = data[staffid]["invites"]
            messages = data[staffid]["messages"]
            genmessages = data[staffid]["genmessages"]
            # print("Data received.")
            if genmessages >= 150 or gawpoints >= 3 or events >= 1 or invites >= 1 or messages >= 500:
                msg1 = "They are done for the day!"
                msg2 = "They should DM you."
            else:
                msg1 = "They are not done for the day."
                msg2 = "Oof."

            em = discord.Embed(
                title=f"{member.name}'s Staff Reqs",
                description=f"**Giveaway Points:** {data[staffid]['gawpoints']} \n\n **Events:** {data[staffid]['events']} \n\n **Invites:** {data[staffid]['invites']} \n\n **Total Messages:** {data[staffid]['messages']} \n\n **General Messages:** {data[staffid]['genmessages']}",
                color=random_color(),
            )
            em.set_footer(text=f"{msg1} {msg2}")
            await ctx.send(embed=em)
        else:
            await ctx.send("Isn't a staff lol")

    @commands.command()
    @commands.has_role("GOAT 🐐")
    async def resetreqs(self, ctx):
        """Owner-only, used to reset the reqs everyday manually. It should be done automatically now, but just in case..."""

        member = ctx.author
        role = discord.utils.get(member.guild.roles, id=797290799083683902)
        staff = [m.id for m in role.members]
        # print(staff)
        # await message.send(staff)
        try:
            for user_id in staff:
                with open("database/staffdata.json", "r") as f:
                    data = json.load(f)
                user_id = str(user_id)
                data[user_id]["Yesterday Messages"] = data[user_id]["messages"]
                data[user_id]["Yesterday Gawpoints"] = data[user_id]["gawpoints"]
                with open("database/staffdata.json", "w") as f:
                    data = json.dump(data, f, indent=4)

                with open("database/staffdata.json", "r") as f:
                    data = json.load(f)
                data[user_id]["gawpoints"] = 0
                data[user_id]["events"] = 0
                data[user_id]["invites"] = 0
                data[user_id]["messages"] = 0
                data[user_id]["genmessages"] = 0

                with open("database/staffdata.json", "w") as f:
                    data = json.dump(data, f, indent=4)

            await ctx.send("Success! All staff counters have been reset.")
        except:
            traceback.print_exc()

            # return

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def echo(self, ctx, channel: Optional[TextChannel], *, arg=None):
        """
        Sends a specified message in a specified channel. If no channel is provided, the channel will default to the channel the command was sent in.
        """
        if arg == None:
            await ctx.send("You need to send something lmao")

        channel = channel or ctx

        await channel.send(arg, allowed_mentions=discord.AllowedMentions.none())

        await ctx.message.add_reaction("✅")

    @commands.group(name="tally", aliases=["tallies", "tly", "t"])
    async def tally(self, ctx):
        """
        Each week, staff must have at least 4 tallies out of 7 days total.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a subcommand. E.g. `?tally count`, `?tally leaderboard`.")

    @tally.command(name="reset")
    @commands.is_owner()
    async def resettallies(self, ctx):
        member = ctx.author
        role = discord.utils.get(member.guild.roles, id=797290799083683902)
        staff = [m.id for m in role.members]
        for user_id in staff:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)
            try:
                data[str(user_id)]["tallies"] = 0
            except:
                fmt = {"tallies": 0}
                user_id = str(user_id)
                userdata = data[user_id]
                userdata.update(fmt)
            with open("database/staffdata.json", "w") as f:
                data = json.dump(data, f, indent=4)
        await ctx.send("Success, all tallies have been reset.")

    @tally.command(name="add")
    @commands.is_owner()
    async def add_tallies(self, ctx, members: commands.Greedy[discord.Member], amount=1):
        if members == None:
            await ctx.send("Please specify the amount of tallies. Use the format `?addtallies [user] [amount (defaults to 1)]`")
            return

        try:
            amount = int(amount)
        except:
            await ctx.send("Please enter a valid amount of tallies to add.")
            return

        with open("database/staffdata.json", "r") as f:
            data = json.load(f)

        for m in members:
            data[str(m.id)]["tallies"] += amount

        with open("database/staffdata.json", "w") as f:
            data = json.dump(data, f, indent=4)

        await ctx.send("Success.")

    @tally.command(name="count")
    @commands.has_role("⋆ Staff Team")
    async def tally_count(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        try:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)
            await ctx.send(f"{user} has {data[str(user.id)]['tallies']} tallies.")
        except:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)
            fmt = {"tallies": 0}

            user_id = str(user.id)
            userdata = data[user_id]
            userdata.update(fmt)

            await ctx.send(f"{user} has 0 tallies.")

            with open("database/staffdata.json", "w") as f:
                data = json.dump(data, f, indent=4)

    @tally.command(name="lb", aliases=["leaderboard"])
    async def tallylb(self, ctx):
        try:
            # print("heard command")
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)

            leader_board = {}
            total = []
            # print("hi")
            # username = client.get_user(541482948155670548)
            # print(username)

            for user in data:
                name = int(user)
                # print(name)
                total_amount = data[user]["tallies"]
                if total_amount in total:
                    leader_board[total_amount].append(name)
                else:
                    leader_board[total_amount] = [name]
                total.append(total_amount)

            total = sorted(total, reverse=True)

            em = discord.Embed(
                title="All Staff",
                description="This is decided by the amount of tallies that each staff has.",
                color=0x0000FF,
            )
            # await ctx.send(embed = em)
            index = 1
            x = 0
            prevamt = 0
            newamt = 0
            for amt in total:
                newamt = amt
                if newamt == prevamt:
                    pass
                else:
                    x = 0
                # for id_ in leader_board[amt]:
                # print(f"{amt} {x}")
                id_ = leader_board[amt][x]
                member = ctx.guild.get_member(id_)
                name = member.name
                em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
                x += 1

                if index == 18:
                    break
                else:
                    index += 1
                prevamt = amt

            await ctx.channel.send(embed=em)
        except:
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def updatereqs(self, ctx):
        """
        Owner-only, appends new staff members to the staff database, or removes retired staff members.
        """

        member = ctx.author
        role = discord.utils.get(member.guild.roles, id=797290799083683902)
        staff = [m.id for m in role.members]
        # print(staff)
        # await message.send(staff)
        for user_id in staff:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)
            str_user_id = str(user_id)
            if str_user_id in data:
                pass
            else:
                fmt = {
                    "gawpoints": 0,
                    "events": 0,
                    "invites": 0,
                    "messages": 0,
                    "genmessages": 0,
                    "tallies": 0,
                    "All Time Messages": 0,
                    "Weekly Messages": 0,
                    "Yesterday Messages": 0,
                    "All Time Gawpoints": 0,
                    "Weekly Gawpoints": 0,
                    "Yesterday Gawpoints": 0,
                    "All Time Genmessages": 0,
                    "Weekly Genmessages": 0,
                    "Yesterday Genmessages": 0,
                }

                data[str_user_id] = fmt

                with open("database/staffdata.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                username = await self.bot.fetch_user(user_id)
                username = username.name
                # print(username)
                await ctx.send(f"Added counters for {username}.")
                await asyncio.sleep(0.5)
                continue
        for userid in data:
            with open("database/staffdata.json", "r") as f:
                data = json.load(f)
            if int(userid) in staff:
                pass
            else:
                del data[userid]
                await ctx.send(f"Removed counters for <@!{userid}>.")
                with open("database/staffdata.json", "w") as f:
                    data = json.dump(data, f, indent=4)
                await asyncio.sleep(0.5)
                continue
        em = discord.Embed(
            title="Success! :D",
            description="All missing staff have been successfully filled in, and all retired staff have been removed.",
            color=random_color(),
        )
        await ctx.send(embed=em)

        # return

    @commands.command()
    @commands.is_owner()
    async def setdelay(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.guild.id == 797250683430633512:
            if message.author.bot:
                return
            member = message.author
            role = message.guild.get_role(797290799083683902)
            staff = [str(m.id) for m in role.members]
            message_author = str(member.id)
            staffreqchannel = self.bot.get_channel(827278383955181578)

            with open("database/staffdata.json", "r") as f:
                data = json.load(f)

            if message_author in staff:
                if message_author in staff:
                    if message.channel.id == 797250683430633517:
                        data[message_author]["messages"] += 1
                        data[message_author]["Weekly Messages"] += 1
                        data[message_author]["genmessages"] += 1
                        data[message_author]["All Time Messages"] += 1
                        data[message_author]["Weekly Genmessages"] += 1
                        data[message_author]["All Time Genmessages"] += 1
                    else:
                        data[message_author]["messages"] += 1
                        data[message_author]["All Time Messages"] += 1
                        data[message_author]["Weekly Messages"] += 1
                        if message.channel.id == 799400771741155390:
                            data[message_author]["messages"] -= 1
                            data[message_author]["All Time Messages"] -= 1
                            data[message_author]["Weekly Messages"] -= 1
                    with open("database/staffdata.json", "w") as f:
                        json.dump(data, f, indent=4)
                if (
                    "<@&799362672755474492>" in message.content
                    or "<@&803500150537977867>" in message.content
                    or "<@&813510883481354290>" in message.content
                    or "giveaway starting" in message.content.lower()
                ):
                    if message.channel.id == 816730128570384424:
                        giveawayformat = "Large Giveaway"
                        giveawaypoints = 2
                        data[message_author]["gawpoints"] += giveawaypoints
                        data[message_author]["All Time Gawpoints"] += giveawaypoints
                        data[message_author]["Weekly Gawpoints"] += giveawaypoints
                        with open("database/staffdata.json", "w") as f:
                            json.dump(data, f, indent=4)
                        with open("database/staffdata.json", "r") as f:
                            data = json.load(f)
                        em = discord.Embed(
                            title="Giveaway Point(s) Earned.",
                            description=f"By creating a {giveawayformat}, {message.author} has earned {giveawaypoints} giveaway points!",
                            color=discord.Color.green(),
                        )
                        em.set_footer(text=f"{message.author} now has {data[message_author]['gawpoints']} giveaway points.")
                        with open("database/staffdata.json", "w") as f:
                            json.dump(data, f, indent=4)
                    if message.channel.id == 798105682377048064:
                        giveawayformat = "Small Giveaway"
                        giveawaypoints = 1
                        data[message_author]["gawpoints"] += giveawaypoints
                        data[message_author]["All Time Gawpoints"] += giveawaypoints
                        data[message_author]["Weekly Gawpoints"] += giveawaypoints
                        with open("database/staffdata.json", "w") as f:
                            json.dump(data, f, indent=4)
                        with open("database/staffdata.json", "r") as f:
                            data = json.load(f)
                        em = discord.Embed(
                            title="Giveaway Point(s) Earned.",
                            description=f"By creating a {giveawayformat}, {message.author} has earned {giveawaypoints} giveaway points!",
                            color=discord.Color.green(),
                        )
                        em.set_footer(text=f"{message.author} now has {data[message_author]['gawpoints']} giveaway points.")
                        with open("database/staffdata.json", "w") as f:
                            json.dump(data, f, indent=4)
                    await staffreqchannel.send(embed=em)
                if message.channel.id == 801917409279606844:
                    if "<@&801878923582373958>" in message.content and "event starting" in message.content.lower():
                        data[message_author]["events"] += 1
                        em = discord.Embed(
                            title="Event Hosted",
                            description=f"By hosting an event, {message.author} has earned 1 event point!",
                            color=discord.Color.green(),
                        )
                        em.set_footer(text=f"{message.author} has hosted {data[message_author]['events']} event(s) today.")
                        with open("database/staffdata.json", "w") as f:
                            json.dump(data, f, indent=4)
                        await staffreqchannel.send(embed=em)
                # if message.channel.id == 803668065946042368:
                #   if "https://discord.gg" in message.content:
                #     with open("partnerships.json", "r") as f:
                #       data = json.load(f)
                #     try:
                #       data[str(message.author.id)]['count'] += 1
                #     except:
                #       fmt = {
                #         'count': 0
                #       }
                #       data[str(message.author.id)] = fmt
                #       data[str(message.author.id)]['count'] += 1
                #       with open("partnerships.json", "w") as f:
                #         json.dump(data, f, indent=4)
                #     count = data[str(message.author.id)]['count']
                #     em = discord.Embed(title = f"Partnership by {message.author.name}", description = f"Thank you {message.author.mention} for the new partnership! \nPartner Count: `{count}`", color = discord.Color.green())
                #     await message.channel.send(message.author.mention, embed = em)

            # if message.channel.id == 828023710073225257:
            #   response =  rs.get_ai_response(f"{message.content}")
            #   await message.reply(response, mention_author=False) #DISABLED

            if message.content == "<@!783216602849607681>":
                await message.channel.send("Hey there! I'm Penguin bot! My prefix is `?`")

        else:
            pass


def setup(bot):
    bot.add_cog(Staff(bot))
