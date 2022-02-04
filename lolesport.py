import os
from dotenv import load_dotenv
from discord.ext import commands
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
async def schedule(ctx, arg1):
    await ctx.send(loldata.filtered_matches(max=10, to_string=True, filter=arg1))

bot.run(token)