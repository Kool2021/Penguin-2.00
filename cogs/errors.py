import datetime

import discord
from discord.ext import commands, menus


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # sourcery no-metrics

        if hasattr(
            ctx.command, "on_error"
        ) or (  # this just checks if the command has its own error handler, or the cog has its own error handler
            ctx.command and hasattr(ctx.cog, f"_{ctx.command.cog_name}__error")
        ):
            return

        error = getattr(error, "original", error)

        ignored_errors = (commands.CommandNotFound,)

        not_found_errors = (  # these are raised when you couldnt find someone, e.g if you did `?kick dskfjdskjfhdksjfhdjk` it would say that it couldn't find that member
            commands.MemberNotFound,
            commands.GuildNotFound,
            commands.RoleNotFound,
            commands.ChannelNotFound,
            commands.EmojiNotFound,
            commands.UserNotFound,
            commands.MessageNotFound,
        )

        async def send_error_embed(
            _desc,
        ):  # too lazy to write out a full embed thing for each error so I did this, just ignore it
            errorEmbed = discord.Embed(
                title=f"Error",
                description=_desc,
                color=discord.Color.dark_red(),
                timestamp=ctx.message.created_at,
            )
            await ctx.send(embed=errorEmbed)

        if isinstance(error, ignored_errors):  # who cares abt these errors
            return

        elif isinstance(error, commands.CommandOnCooldown):

            def custom_format(td):
                minutes, seconds = divmod(td.seconds, 60)
                hours, minutes = divmod(minutes, 60)
                return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)

            cooldown1 = datetime.timedelta(seconds=error.retry_after)
            cooldown1 = str(custom_format(cooldown1))
            em = discord.Embed(
                title=f"Lmao you should prolly chill",
                description=f"{ctx.author.mention} You're still on kooldown, please try again in **{cooldown1}**.",
            )
            return await ctx.send(embed=em)

        elif isinstance(
            error,
            commands.MissingPermissions,  # author missing permissions. e.g if a command had `@commands.has_permissions(administrator)` on it, then if a non admin tried to do it, this would send a message
        ):
            msg = (
                f"You need the "
                + ", ".join([perm.replace("_", " ").replace("guild", "server") for perm in error.missing_perms])
                + " permission(s) to carry out that command!\nTry again when you have them."
            )
            return await send_error_embed(msg)

        elif isinstance(
            error,
            commands.BotMissingPermissions,  # same thing, but the bot itself is missing permissions to do something
        ):
            msg = (
                f"I need the "
                + ", ".join([perm.replace("_", " ").replace("guild", "server") for perm in error.missing_perms])
                + " permission(s) to carry out that command!\nPlease give them to me and try again."
            )
            return await send_error_embed(msg)

        elif isinstance(
            error,
            commands.MissingRequiredArgument  # when missing argument, e.g `?echo` without an actual message.
            # This eliminates the need to write all those "Please use the format `?bully [user] [reason]`" messages
        ):
            await ctx.send(
                str(error) + f"\nPlease use the format: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`"
            )

        elif isinstance(error, commands.NotOwner):
            msg = "Only the owner of Penguin can use this command."
            return await send_error_embed(msg)

        elif isinstance(error, commands.CheckFailure):
            msg = "You don't have the permissions needed to do that"
            return await send_error_embed(msg)

        elif isinstance(
            error,
            discord.Forbidden,  # something you cant do, like change the server owners nickname
        ):
            return

        elif isinstance(error, commands.BadArgument):  # usually improper arguments
            return await send_error_embed(str(error))

        elif isinstance(error, not_found_errors):
            return await ctx.send(str(error))

        elif isinstance(error, menus.MenuError):  # any menu error
            return await ctx.send(str(error))

        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.send("Chill, you can' use that command as it is already running.")

        else:
            await send_error_embed(
                f"Ignoring Exception in command {ctx.command.name}:\n```\n{error}\n```"
            )  # sends the basic error, check terminal for full error
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
