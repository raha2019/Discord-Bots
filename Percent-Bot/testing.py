import pandas as pd
import csv
import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='Testing your code'))

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

client.run('XXXXXX')