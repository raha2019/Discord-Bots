import discord
from discord.ext import commands

client = commands.Bot(command_prefix= '.')

@client.event
async def on_ready():
    print('Bot has connected')

@client.command()
async def log(ctx, arg):
    print(arg)
    changeLog = open("changelog.txt", "a+")

    await ctx.send(arg + " **Test**")



client.run('XXXXXX')