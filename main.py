import discord
from discord.ext import commands
import datetime

intents = discord.Intents.all()
intents.members = True

initial_extensions = (
    "jishaku",
    "cogs.staff",
    "cogs.misc",
    "cogs.fun",
    "cogs.errors",
    "cogs.help",
    "cogs.utility",
    "cogs.chugsroyale",
    "cogs.tasks",
    "cogs.events",
    "cogs.test",
)


_activity = discord.Activity(type=discord.ActivityType.watching, name="over The Arctic")


class Penguin(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("?"),
            case_insensitive=True,
            intents=intents,
            activity=_activity,
            status=discord.Status.idle,
        )

        self.delete_invites = True
        for ext in initial_extensions:
            self.load_extension(ext)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print(f"Running on discord.py {discord.__version__}")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("Bot has connected to Discord.")
        print("------")


if __name__ == "__main__":
    bot = Penguin()
    bot.run("TOKEN")
