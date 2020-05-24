# coding=utf-8


#---------------------------- ideas ----------------------------#
# limit giving points to once a minute
# put a time when last points given as a column
# put a ban thing in the database as a column
# implement ban and unban methods
# implement leaderboard method, call it points_top
# implement set_points method
# implement exception handling
#---------------------------------------------------------------#


import asyncio
import pathlib
import sqlite3

import discord
from discord.ext import commands

from utils import print_context


class RankingCog(commands.Cog, name='Ranking Commands'):
    """ranking cog"""

    def __init__(self, bot: commands.Bot) -> None:
        """initializer"""

        self.bot = bot
        self.db_path = pathlib.Path('./points_db.sqlite3').resolve()

    async def db_connect(self):
        con = sqlite3.connect(self.db_path)
        return con

    @commands.command()
    @commands.is_owner()
    @print_context
    async def points_give(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
            points: int = None,
            reason: str = 'no reason'
    ) -> None:
        """give a member points"""

        if not member:
            await ctx.send('**`member not specified or not found`**')
            return
        if not points:
            await ctx.send('**`points not specified or points was 0`**')
            return
        if not -100 <= points <= 100:
            await ctx.send('**`points not in valid range -100 <= points <= 100`**')
            return
        if ctx.author.id == member.id and ctx.author.id != self.bot.owner_id:
            await ctx.send("**`You can't high-five yourself!`**")
            return

        con = await self.db_connect()
        with con:
            cur = con.cursor()

            # create server table if needed
            create_server_table = f'''
                CREATE TABLE IF NOT EXISTS server_{ctx.guild.id} (
                member_id integer PRIMARY KEY,
                points integer NOT NULL DEFAULT 0
                )'''
            cur.execute(create_server_table)

            # create member row if needed
            cur.execute(
                f'INSERT OR IGNORE INTO server_{ctx.guild.id} (member_id) VALUES(?)',
                (member.id,)
            )

            # update points for member
            cur.execute(
                f'UPDATE server_{ctx.guild.id} SET points = points + ? WHERE member_id = ?',
                (points, member.id)
            )

            # get member's new point total
            cur.execute(
                f'SELECT * from server_{ctx.guild.id} where member_id = ?',
                (member.id, )
            )
            total_points = cur.fetchone()[1]

            await ctx.send(
                f'**`{points} points were given to {member.display_name} for {reason}! '
                f'They now have {total_points} points!`**'
            )

    @commands.command()
    @print_context
    async def points_show(
            self,
            ctx: commands.Context,
            member: discord.Member = None,
    ) -> None:
        """display a member's points"""

        con = await self.db_connect()
        with con:
            cur = con.cursor()

            # create server table if needed
            create_server_table = f'''
                CREATE TABLE IF NOT EXISTS server_{ctx.guild.id} (
                member_id integer PRIMARY KEY,
                points integer NOT NULL DEFAULT 0
                )'''
            cur.execute(create_server_table)

            # create member row if needed
            cur.execute(
                f'INSERT OR IGNORE INTO server_{ctx.guild.id} (member_id) VALUES(?)',
                (member.id,)
            )

            # get member's point total
            cur.execute(
                f'SELECT * from server_{ctx.guild.id} where member_id = ?',
                (member.id, )
            )
            total_points = cur.fetchone()[1]

            await ctx.send(f'**`{member.display_name} has {total_points} points`**')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(RankingCog(bot))
