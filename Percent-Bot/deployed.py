import pandas as pd
import csv
import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = commands.Bot(command_prefix= '.')

df = pd.read_csv("data.csv") 
print(f'finished read in the file')
print(df)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='Stealing Your Money'))

@client.command(pass_context=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=10)
        # await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")

@client.command()
async def create(ctx, name: str, amount: int):
    # await ctx.send('You passed {} and {}'.format(name, str(amount)))
    with open('data.csv', mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([name, str(amount)])
    await ctx.channel.purge(limit=3)
    # await ctx.message.delete()
    df = pd.read_csv("data.csv", index_col='Name') 
    print(f'finished read in the file')
    print(df)   
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    df['Percent'] = pd.eval('df.Amount/totalAmount*100')
    print(df)
    df.to_csv(r'percentage.csv')    
    print(df)
    df = pd.read_csv('percentage.csv')
    df = df.to_string()
    await ctx.send(df)
    # Total Function
    df = pd.read_csv("data.csv", index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    await ctx.send(" Total Amount " + str(totalAmount))
    await channel.send('{} created {} who has {} dollars'.format(ctx.author.mention, name, amount))

@client.command()
async def delete(ctx, index: int):
    information = int(index)
    df = pd.read_csv("data.csv", index_col='Name') 
    print(df)
    df2 = (df.drop(df.index[information]))
    df2.to_csv('data.csv')
    await ctx.channel.purge(limit=3)
    df = pd.read_csv("data.csv", index_col='Name') 
    print(f'finished read in the file')
    print(df)   
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    df['Percent'] = pd.eval('df.Amount/totalAmount*100')
    print(df)
    df.to_csv(r'percentage.csv')    
    print(df)
    df = pd.read_csv('percentage.csv')
    df = df.to_string()
    await ctx.send(df)
    # Total Function
    df = pd.read_csv("data.csv", index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    await ctx.send(" Total Amount " + str(totalAmount))
    await channel.send('{} delete {}'.format(ctx.author.mention, index))

@client.command()
async def total(ctx):
    await ctx.channel.purge(limit=5)
    await ctx.message.delete()
    df = pd.read_csv("data.csv", index_col='Name') 
    print(f'finished read in the file')
    print(df)   
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    df['Percent'] = pd.eval('df.Amount/totalAmount*100')
    print(df)
    df.to_csv(r'percentage.csv')    
    print(df)
    df = pd.read_csv('percentage.csv')
    df = df.to_string()
    await ctx.send(df)
    # Total Function
    df = pd.read_csv("data.csv", index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    await ctx.send(" Total Amount " + str(totalAmount))
    await channel.send('{} called Total Function'.format(ctx.author.mention))

@client.command()
async def change(ctx, index: int, amount: int):
    row = int(index)
    amount = int(amount)
    df = pd.read_csv('data.csv', index_col='Name')
    df['Amount'][row] = amount
    df.to_csv('data.csv')
    #Total Function To be Changed
    await ctx.channel.purge(limit=3)
    df = pd.read_csv("data.csv", index_col='Name') 
    print(f'finished read in the file')
    print(df)   
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    df['Percent'] = pd.eval('df.Amount/totalAmount*100')
    print(df)
    df.to_csv(r'percentage.csv')    
    print(df)
    df = pd.read_csv('percentage.csv')
    df = df.to_string()
    await ctx.send(df)
    # Total Function
    df = pd.read_csv("data.csv", index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    await ctx.send(" Total Amount " + str(totalAmount))
    await channel.send('{} Changed {} to {}'.format(ctx.author.mention, row, amount))


@client.command()
async def earnings(ctx, amount: int):
    await ctx.channel.purge(limit=3)
    amount = int(amount)
    def earnings(earning):
        return float(earning / 100 * amount)
    df = pd.read_csv('percentage.csv', index_col='Name')
    rows = int(len(df.index))
    df['Amount'] = df['Percent'].apply(earnings)
    print(df)
    df.to_csv('percentage.csv')
    df2 = df.drop(columns=['Percent'])
    df2.to_csv('data.csv')
    df = pd.read_csv('percentage.csv')
    df = df.to_string()
    await ctx.send(df)
    df = pd.read_csv("data.csv", index_col='Name') 
    totalAmount = df['Amount'].sum()
    print(totalAmount)
    await ctx.send(" Total Amount " + str(totalAmount))
    channel = client.get_channel(675482064493084682)
    await channel.send('{} changed total amount to {}'.format(ctx.author.mention, amount))


client.run('Njc2OTMwNTQ1NjUzMTIxMDQx.XknbIA.SoMNxczEQ7MBpuJ-NUZAk9-x17s')