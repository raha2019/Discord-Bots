import datetime
from datetime import date
import time
import discord
from discord.ext import commands

client = commands.Bot(command_prefix= '.')

def writeVersion():
    changeLogVersion = open("version.txt", "r")
    version = changeLogVersion.read()
    intVersion = int(version)
    intVersion = intVersion + 1
    changeLogVersion.close()
    changeLogVersion = open("version.txt", "w")
    strVersion = str(intVersion)
    changeLogVersion.write(strVersion)
    changeLogVersion.close()
    return strVersion

@client.event
async def on_ready():
    print('Bot has connected')

@client.command()
async def log(ctx, *, arg):
    await ctx.message.delete()
    today = date.today()
    date_object = today.strftime("%d/%m/%Y")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(arg)
    version = writeVersion()
    print(version)
    allLogs = "**Changelog v" + version + " - " + str(date_object) + " - " + str(current_time) + " EST**" + "\n" + arg + "\n"  
    changeLog = open("changelog.txt", "a+")
    changeLog.writelines(allLogs)
    changeLog.close()
    await ctx.send(allLogs)

client.run('XXXXXX')