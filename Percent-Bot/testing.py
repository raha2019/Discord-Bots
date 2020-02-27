import pandas as pd
import csv
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from yahoo_fin import stock_info as si


print(si.get_live_price("qqq"))


client = commands.Bot(command_prefix= '.')

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='Testing your code'))

@client.command()
async def test(ctx, arg):
    await ctx.send(testing)
    await ctx.send(arg)

@client.command(pass_context=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=10)
        # print("this works")
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

client.run(token)