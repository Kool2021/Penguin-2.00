import json
from datetime import datetime

import pytz
from discord.ext import commands, tasks


class Tasks(commands.Cog):
    """Ignore this, this contains no commands, I'll remove this soon"""

    def __init__(self, bot):
        self.bot = bot
        self.reset_reqs_check.start()

    def cog_unload(self):
        self.reset_reqs_check.cancel()

    @tasks.loop(minutes=30)
    async def reset_reqs_check(self):
        await self.bot.wait_until_ready()
        with open("database/dailyloops.json", "r") as f:
            data = json.load(f)
        channel = self.bot.get_channel(797290610737676318)
        tz = pytz.timezone("US/Pacific")
        if data["staff_reqs"]["date"] == "":
            data["staff_reqs"]["date"] = tz.localize(datetime.today()).strftime("%Y-%m-%d")

        elif data["staff_reqs"]["date"] != tz.localize(datetime.today()).strftime("%Y-%m-%d"):
            role = self.bot.get_guild(797250683430633512).get_role(797290799083683902)
            staff = [m.id for m in role.members]
            for user_id in staff:
                with open("database/staffdata.json", "r") as f:
                    data1 = json.load(f)
                user_id = str(user_id)
                data1[user_id]["Yesterday Messages"] = data1[user_id]["messages"]
                data1[user_id]["Yesterday Gawpoints"] = data1[user_id]["gawpoints"]
                with open("database/staffdata.json", "w") as f:
                    data1 = json.dump(data1, f, indent=4)

                with open("database/staffdata.json", "r") as f:
                    data1 = json.load(f)
                data1[user_id]["gawpoints"] = 0
                data1[user_id]["events"] = 0
                data1[user_id]["invites"] = 0
                data1[user_id]["messages"] = 0
                data1[user_id]["genmessages"] = 0
                with open("database/staffdata.json", "w") as f:
                    data1 = json.dump(data1, f, indent=4)
            data["staff_reqs"]["date"] = tz.localize(datetime.today()).strftime("%Y-%m-%d")
            await channel.send("All reqs have been reset automatically!")
        with open("database/dailyloops.json", "w") as f:
            data = json.dump(data, f, indent=4)


def setup(bot):
    bot.add_cog(Tasks(bot))
