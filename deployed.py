# Actually Main
import re
import csv
import discord
import pandas as pd 
from dotenv import load_dotenv

while True: 
    load_dotenv()
    token = 'XXXXXXXXX'

    client = discord.Client()

    df = pd.read_csv("data.csv") 
    print(f'finsihed read in the file')
    print(df)

    def calculate():
        df = pd.read_csv("data.csv", index_col='Name') 
        print(f'finished read in the file')
        print(df)   
        totalAmount = df['Amount'].sum()
        print(totalAmount)
        df['Percent'] = pd.eval('df.Amount/totalAmount*100')
        print(df)
        df.to_csv(r'percentage.csv')    
        print(df)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')
        await client.change_presence(activity=discord.Game(name='Stealing Your Money'))


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 

        if message.content.startswith('!create'):
            a = 0
            while a < 2: a = a + 1; await message.delete()
            newMessage = message.content.split(' ', 1)[1]
            print(newMessage)
            content = newMessage.split(" ")
            name = content[0]
            dollarMessage = content[1]
            with open('data.csv', mode='a') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow([name, dollarMessage])
            calculate()
            df = pd.read_csv("percentage.csv", index_col='Name') 
            await message.channel.send(df)
            df = pd.read_csv("data.csv", index_col='Name') 
            totalAmount = df['Amount'].sum()
            await message.channel.send("Total Amount " + str(totalAmount))
            
        if message.content.startswith('!calculate'):
            calculate()
        
        if message.content.startswith('!change'): 
            await message.delete()
            newMessage = message.content.split(' ', 1)[1]
            print(newMessage)
            content = newMessage.split(" ")
            row = str(content[0])
            print(row)
            row = int(row)
            dollarMessage = int(content[1])
            df = pd.read_csv('data.csv', index_col='Name')
            df['Amount'][row] = dollarMessage
            df.to_csv('data.csv')
            calculate()
            df = pd.read_csv("percentage.csv", index_col='Name') 
            await message.channel.send(df)
            df = pd.read_csv("data.csv", index_col='Name') 
            totalAmount = df['Amount'].sum()
            await message.channel.send("Total Amount " + str(totalAmount))

        if message.content.startswith('!delete'):
            await message.delete()
            newMessage = message.content.split(' ', 1)[1]
            print(newMessage)
            content = newMessage.split(" ")
            information = int(content[0])
            df = pd.read_csv("data.csv", index_col='Name') 
            print(df)
            df2 = (df.drop(df.index[information]))
            df2.to_csv('data.csv')
            calculate()
            await message.channel.send(str(information) + ' has been deleted')
            df = pd.read_csv("data.csv", index_col='Name') 
            totalAmount = df['Amount'].sum()
            await message.channel.send("Total Amount " + str(totalAmount))
        
        if message.content.startswith('!total'):
            await message.delete()
            # All Function
            df = pd.read_csv('percentage.csv')
            calculate()
            await message.channel.send(df)
            # Total Function
            df = pd.read_csv("data.csv", index_col='Name') 
            totalAmount = df['Amount'].sum()
            print(totalAmount)
            await message.channel.send("Total Amount " + str(totalAmount))

        if message.content.startswith('!all'): 
            await message.delete()
            commands = """Commands: 
                            !create: 
                                Format:
                                    !create Name Amount
                                Example:
                                    !create Vikram 500
                            !change:
                                Format:
                                    !change Name Amount
                                Example:
                                    !change 0 500
                            !delete:
                                Format:
                                    !delete index
                                    index is the number next to each name on the right in the total message
                                Example:
                                    !delete 0
                            !total:
                                Format:
                                    !total
                                Example:
                                    !total"""
            await message.channel.send(commands)
            
        
    client.run(token)