import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from loldata import LOLData

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
loldata = LOLData()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='about')
async def about(ctx):
    await ctx.send('Pleased to meet you!')

@bot.command(name='schedule')
async def schedule(ctx, *args):
    regions = 'global'
    if args.__len__() >= 1:
        regions = args
    # print(regions)
    await ctx.send(loldata.filtered_matches(max=10, to_string=True, regions=regions))

@bot.command()
async def test(ctx, *args):
    regions = 'global'
    if args.__len__() >= 1:
        regions = args
    await ctx.send(file=discord.File(loldata.filtered_matches_image(regions=regions)))
""" 
TODO: 
    - standings, 
    - games start notification, 
    - games finish notification, 
    - roster changes notifications, 
    - lines up
"""
bot.run(token)