import random

import discord
from discord.ext import commands

colors = [0xCAF7E3, 0xF8EDED, 0xF6DFEB, 0xE4BAD4]


# Unimportant part
class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help",
            description=f"`{self.clean_prefix}help [command]` will send help for a certain command, `{self.clean_prefix}help [category]` will send help for a certain category.",
            color=random.choice(colors),
        )
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            for command in command_signatures:
                command_signatures[command_signatures.index(command)] = f"`{command}`"
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name == "Help" or cog_name == "No Category":
                    continue
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        cog_commands = [
            self.get_command_signature(c) for c in await self.filter_commands(cog.walk_commands(), sort=True)
        ]
        cog_name = getattr(cog, "qualified_name", "No Category")
        for command in cog_commands:
            cog_commands[cog_commands.index(command)] = f"`{command}`"
        embed = discord.Embed(
            title=f"{cog_name} Help", description="\n".join(cog_commands), color=random.choice(colors)
        )
        embed.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.avatar_url)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=random.choice(colors))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Focus here
        # Setting the cog for the help
        help_command = MyHelp()
        help_command.cog = self  # Instance of YourCog class
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(Help(bot))
