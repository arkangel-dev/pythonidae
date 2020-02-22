#!/usr/bin/env python
# coding=utf-8


import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_TESTING')

bot = commands.Bot(command_prefix='!')


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='99', help='responds with a random quote from brooklyn nine-nine')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='simulates rolling dice')
async def roll(ctx, number_of_dice: int = None, number_of_sides: int = None):
    number_of_dice = number_of_dice or 1
    number_of_sides = number_of_sides or 6
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('you do not have the correct role for this command')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord', flush=True)
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f"{bot.user} is connected to the following guild:")
    print(f"{guild.name} (id: {guild.id})")
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild members:\n - {members}", flush=True)


if __name__ == '__main__':
    bot.run(TOKEN)
