import json
import random
import traceback

import aiosqlite
import discord
from discord.ext import commands, menus


color_palette = [0x66FF00, 0x1974D2, 0x08E8DE, 0xFFF000, 0xFFAA1D, 0xFF007F]


def random_color():
    return random.choice(color_palette)


selected_soda = ""


class TestRegularPagSource(menus.ListPageSource):
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
            color=random_color(),
        )
        em.set_footer(text=f"Page {menu.current_page+1}/{self.get_max_pages()}")
        global selected_soda
        selected_soda = sodadata[sodainv[offset]]["name"]
        return em


class TestRegularPages(menus.MenuPages):
    @menus.button("👍")
    async def select(self, payload):
        try:
            await self.message.delete()
            self.stop()
            p2 = TestRegularPages2()
            await p2.start(self.ctx)
        except:
            traceback.print_exc()

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def end_menu(self, _):
        await self.message.delete()
        self.stop()


class TestRegularPages2(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        global selected_soda
        em = discord.Embed(
            title="Confirmation",
            description=f"Are you sure you want to select this soda? `{selected_soda}`",
            color=random_color(),
        )
        return await ctx.send(embed=em)

    @menus.button("✅")
    async def yes(self, payload):
        global selected_soda
        await self.message.edit(
            embed=discord.Embed(
                title="Success!",
                description=f"You have selected `{selected_soda}` to be chugged.",
                color=random_color(),
            )
        )
        await self.message.clear_reactions()

    @menus.button("❌")
    async def no(self, payload):
        with open("database/sodagame.json", "r") as f:
            data = json.load(f)
        sodainv = data[str(self.ctx.author.id)]["soda inventory"]
        source = TestRegularPagSource(range(1, len(sodainv) + 1), sodas={})
        p = TestRegularPages(source)
        await self.message.delete()
        self.stop()
        return await p.start(self.ctx)


class TestCog(commands.Cog):
    """Test Cog for New Features"""

    def __init__(self, bot):
        self.bot = bot

    class TestMenu(menus.Menu):
        async def send_initial_message(self, ctx, channel):
            with open("database/sodagame.json", "r") as f:
                data = json.load(f)
            sodainv = data[str(self.ctx.author.id)]["soda inventory"]
            if sodainv == []:
                em = discord.Embed(
                    title="No Sodas!",
                    description="You don't have any sodas in your inventory! Do `?search` to find some!",
                    color=random_color(),
                )
                return await ctx.send(embed=em)
            if len(sodainv) == 1:
                em = discord.Embed(
                    title="Not Enough Sodas!",
                    description="You need at least **2** sodas in your inventory to perform! Do `?search` to find some!",
                    color=random_color(),
                )
                return await ctx.send(embed=em)
            source = TestRegularPagSource(range(1, len(sodainv) + 1))
            p = TestRegularPages(source)
            await p.start(self.ctx)

    @commands.command()
    @commands.is_owner()
    async def create_table(self, ctx, db_file, name, *, columns):
        try:
            my_list = columns.split(", ")
            db_file = f"database/{db_file}.db"
            conn = await aiosqlite.connect(db_file)
            execute_cmd = f"""CREATE TABLE {name}
                        (ID INT PRIMARY KEY NOT NULL,
                        """
            for column in my_list:
                if my_list.index(column) == len(my_list) - 1:
                    column = column.replace("-", " ")
                    execute_cmd += f" {column})"
                else:
                    column = column.replace("-", " ")
                    execute_cmd += f" {column},\n"
            await conn.execute(execute_cmd)

            await conn.close()
            await ctx.send(f"Successfully created table called {db_file}")
        except:
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def input_values(self, ctx, db_file, value, value2, value3):
        db_file = f"database/{db_file}.db"
        conn = await aiosqlite.connect(db_file)
        print("Opened database successfully")
        try:
            await conn.execute(
                f"INSERT INTO SODAGAME (ID, WALLET, BANK) \
                VALUES ({value}, {value2}, {value3})"
            )

            await conn.commit()
            await ctx.send("Records created successfully")
            await conn.close()
        except:
            traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    async def update_bank(self, ctx, user: discord.Member, change):
        db_file = "database/sodagame.db"
        conn = await aiosqlite.connect(db_file)
        await conn.execute(f"UPDATE SODAGAME SET WALLET = WALLET + {int(change)} WHERE ID = {user.id}")
        await conn.commit()
        await ctx.send("Records updated successfully")
        await conn.close()

    @commands.command()
    @commands.is_owner()
    async def print_data(self, ctx, db_file):
        try:
            db_file = f"database/{db_file}.db"
            conn = await aiosqlite.connect(db_file)
            cursor = await conn.execute("SELECT id, wallet from SODAGAME")
            cursor1 = await cursor.fetchall()
            for row in cursor1:
                await ctx.send(f"{row[0]} Balance: {row[1]}")
            await conn.close()
        except:
            traceback.print_exc()


def setup(bot):
    bot.add_cog(TestCog(bot))
