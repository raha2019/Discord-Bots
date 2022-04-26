## Code that has been tested and is able to be deployed 

from os import close
import os
import logging

import pandas as pd
import csv
import datetime
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from tabulate import tabulate

import discord
import discord.utils
from discord import channel
from discord.ext.commands import Bot
from discord.ext import commands

# Starting Sequence
client = commands.Bot(command_prefix= '!')

## Declaring global variables ##
global raw_data # = "data/data.csv"
global percentageData # = "data/percentage.csv"
global balanceData # = "balance.csv"
global logs

raw_data = ''
percentData = ''
balanceData = ''
logs = ''

global logChannel 
global holdingsChannel
global accountProgressChannel
global guildID

guildID = ''

global logger


# ************** Should look for the available files or create one if it doesn't exist 
# Check if required channels are there and then create global variables

# Returns the Value from the table
async def getTotal():
    # Gets Table of Values
    print(raw_data)
    df = pd.read_csv(raw_data, index_col='Name') 
    print(f'finished read in the file')
    # print(df)   
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    df['Percent'] = pd.eval('df.Amount/totalAmount*100')
    # print(df)
    df.to_csv(percentageData)    
    # print(df)

    df = pd.read_csv(percentageData)
    df['Name'] = df['Name'].str.pad(15, side = 'both')
    df['Amount'] = df['Amount'].map('${:,.2f}'.format)
    df['Percent'] = df['Percent'].map('{:,.2f}%'.format)
    # tableOfVals = df.to_string()
    tableOfVals = df.to_markdown()
    # tableOfVals = tabulate(df, headers = 'keys', tablefmt = 'psql')
    # tableOfVals = tabulate(df)
    
    # Gets Total Value
    df = pd.read_csv(raw_data, index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    totalAmount = "%.2f" % totalAmount
    return (totalAmount, tableOfVals) 

# Makes a chart that shows investing performance
async def makeChart():
    print("This is being run")
    accountValues = []
    dates  = []
    with open(balanceData, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
            dates.append(row[0])
            accountValues.append(float(row[1]))

    fig, ax = plt.subplots()
    for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    fig.suptitle('AIC Performance')
    ax.plot(dates, accountValues, label="Account Value")
    plt.savefig('chart.png')

# Calcluates the Percent and Dollar Change from the last update
async def percentChange(amount: float):
    previousVal = 0
    with open(balanceData, 'r') as f:
        for row in reversed(list(csv.reader(f, delimiter=','))):
            previousVal = row[1]
            break
    f.close
    print("This is being run")
    percentDif = round((amount - float(previousVal))/float(previousVal) * 100, 2)
    dollarDif = amount - float(previousVal)
    isPositive = True
    if (percentDif < 0):
        isPositive = False
    return (percentDif, dollarDif, isPositive) 

# What happens when the Bot is ready    
@client.event
async def on_ready():
    # Connects 
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='Stealing Your Money || !setup'))

    # Check Data

# Sets up the Bot/Checks the data 
@client.command()
async def setup(ctx):
    guildID = str(ctx.guild.id)

    # Make this into a try catch
    global logChannel
    global holdingsChannel
    global accountProgressChannel

    logChannel = discord.utils.get(ctx.guild.channels, name="logs")
    holdingsChannel = discord.utils.get(ctx.guild.channels, name="holdings")
    accountProgressChannel = discord.utils.get(ctx.guild.channels, name="account-progress")

    if not os.path.isdir(guildID):
        os.mkdir(guildID)

    if not os.path.exists(guildID + '/data.csv'):
        # print("Hello")
        file = open(guildID + '/data.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(["Name", "Amount"])
        writer.writerow(["PlaceHolder", 0])

    if not os.path.exists(guildID + '/percentage.csv'):
        # print("no?")
        file = open(guildID + '/percentage.csv', 'w')
        writer = csv.writer(file)
        writer.writerow(["Name", "Amount", "Percent"])
    
    if not os.path.exists(guildID + '/balance.csv'):
        # print("no?")
        file = open(guildID + '/balance.csv', 'w')
        writer = csv.writer(file)
        today = date.today()
        today = today.strftime("%m/%d/%y")
        writer.writerow([today, 1])

    if not os.path.exists(guildID + '/logs.log'):
        # print("Hello")
        file = open(guildID + '/logs.log', 'w')

    global raw_data
    global percentageData
    global balanceData
    global logs
    
    raw_data = guildID + '/data.csv'
    percentageData = guildID + '/percentage.csv'
    balanceData = guildID + '/balance.csv'
    
    logs = guildID + '/logs.log'
    
    logging.basicConfig(filename=logs,format='%(asctime)s %(message)s',datefmt='%d-%b-%y %H:%M:%S',filemode='a+')
    global logger
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)

    # df = pd.read_csv(raw_data) 

@client.command()
async def listCommands(ctx):
    await ctx.channel.purge(limit=1)

    # Makes Embed
    embed=discord.Embed(title="Commands", description="Lists of Commands", color=0x69f529)
    embed.add_field(name="!create", value="**Format:** !create Name Amount, **Example**: !create Vikram 500", inline=False)
    embed.add_field(name="!change", value="**Format:** !change Index Amount, **Example:** !change 0 500", inline=False)
    embed.add_field(name="!delete", value="**Format:** !delete index; **Example:** !delete 0", inline=False)
    embed.add_field(name="!earnings", value="**Format:** !earnings num; **Example:** !earnings 1360.00", inline=False)
    embed.add_field(name="!holdings", value="Returns current holdings", inline=False)

    await ctx.author.send(embed=embed)

# Command to purge messages in channel
@client.command(pass_context=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=10)
        # await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

# Raises error if message can't be deleted
@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

# Add Member to List
@client.command()
async def create(ctx, name: str, amount: int):
    # await ctx.send('You passed {} and {}'.format(name, str(amount)))
    with open(raw_data, mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([name, str(amount)])
    
    # Deletes Initial Message
    await ctx.channel.purge(limit=1)

    # Prints Out the table
    totalAmount, tableOfVals = await getTotal()
    await ctx.send("```" + tableOfVals + "```")
    await ctx.send(" Total Amount: $" + str(totalAmount))
    
    # Sends Message to Logs
    channel = discord.utils.get(ctx.guild.channels, name="logs")
    logging.info('%s created %s with $%s', ctx.author.name, name, amount)
    await channel.send('{} created {} who has ${}'.format(ctx.author.mention, name, amount))

# Deletes User from the data
@client.command()
async def delete(ctx, index: int):
    information = int(index)
    df = pd.read_csv(raw_data, index_col='Name') 
    name = df.index[information]
    amount = df['Amount'][information]
    # print(df)

            # Make sure to get name 

    df2 = (df.drop(df.index[information]))
    df2.to_csv(raw_data)

    # Deletes the command
    await ctx.channel.purge(limit=1)

    # Prints out the table
    totalAmount, tableOfVals = await getTotal()
    await ctx.send("```" + tableOfVals + "```")
    await ctx.send(" Total Amount: $" + str(totalAmount))
    
    # Sends Message to Logs
    channel = discord.utils.get(ctx.guild.channels, name="logs")
    logging.info('%s deleted %s with $%s', ctx.author.name, name, amount)
    await channel.send('{} delete {} with ${}'.format(ctx.author.mention, name, amount))

# Prints the Table
@client.command()
async def total(ctx):
    # Delete Command Message
    print("Raw data path: " + raw_data)
    await ctx.channel.purge(limit=1)

    # Prints Out the table
    totalAmount, tableOfVals = await getTotal()
    await ctx.send("```" + tableOfVals + "```")
    await ctx.send(" Total Amount: $" + str(totalAmount))

    # Send Message to Logs
    channel = discord.utils.get(ctx.guild.channels, name="logs")
    logger.info('%s called total', ctx.author.name)
    # logger.info("Testing")
    await channel.send('{} called Total Function'.format(ctx.author.mention))

# Changes the amount for the requested person
@client.command()
async def change(ctx, index: int, amount: int):
    row = int(index)
    amount = int(amount)
    df = pd.read_csv(raw_data, index_col='Name')

    name = df.index[row]
    df['Amount'][row] = amount
    df.to_csv(raw_data)

    # Deletes Command Message
    await ctx.channel.purge(limit=1)

    # Prints Out the table
    totalAmount, tableOfVals = await getTotal()
    await ctx.send("```" + tableOfVals + "```")
    await ctx.send(" Total Amount: $" + str(totalAmount))

    # Send Message to Logs
    channel = discord.utils.get(ctx.guild.channels, name="logs")
    logging.info('%s change %s to %s', ctx.author.name, name, amount)
    await channel.send('{} Changed {} to {}'.format(ctx.author.mention, name, amount))

""""
@client.command()
async def log(ctx):
    channel = discord.utils.get(ctx.guild.channels, name="holdings")
    await channel.send('Hello {}'.format(ctx.author.mention))
"""

# Change the total number of money
@client.command()
async def earnings(ctx, amount: float):
    # Delete Message
    await ctx.channel.purge(limit=1)
    
    percentDif, dollarDif, isPostive = await percentChange(amount)

    # Recalculates how much money everyone has
    amount = float(amount)
    def earnings(earning):
        return float(earning / 100 * amount)
    df = pd.read_csv(percentageData, index_col='Name')
    rows = int(len(df.index))
    df['Amount'] = df['Percent'].apply(earnings)
    # print(df)
    df.to_csv(percentageData)
    df2 = df.drop(columns=['Percent'])
    df2.to_csv(raw_data)
    
    # Adds Date and Balance to Text File
    today = date.today()
    today = today.strftime("%m/%d/%y")
    with open(balanceData, mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([today, amount])
    
    """ Create a function to check if it is a duplicate value """

    # Prints Out the table to #Holdings (Check if total is in #Holdings)
    totalAmount, tableOfVals = await getTotal()
    await ctx.send("```" + tableOfVals + "```")
    await ctx.send(" Total Amount: $" + str(totalAmount))

    # Makes the Chart and Sends it to appropriate Channel with a percentChange message
    await makeChart()
    # Send Message to # account Progress
    # channel = client.get_channel(746882920702279742) # Change Channels to be dynamic (Holdings) 675480914695946240  (3dp)778362992986554448
    
    channel = discord.utils.get(ctx.guild.channels, name="account-progress") # change to account progress
    if (percentDif == 0.0):
         await channel.send('Playing it cool, smart idea 😎, no need to be risky')
    elif (isPostive): 
        await channel.send('The Account has had a {:.2f}% gain and ${:.2f} gain from last count.'.format(percentDif, dollarDif))
    else: 
        await channel.send('The Account has had a {:.2f}% loss and ${:.2f} loss from last count. Better Luck Next Time!'.format(percentDif, dollarDif))
    
    await channel.send(file=discord.File('chart.png'))

    logging.info('%s change total to %s', ctx.author.name, totalAmount)
    


client.run('XXXXXX')