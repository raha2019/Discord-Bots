# Actually Main
import re
import csv
import discord
import pandas as pd 
from dotenv import load_dotenv

while True: 
        
    load_dotenv()
    token = 'NjcyNjQ5NTIzMDIxMjE3Nzkz.Xjc5bA.qCvw1LA3mEjw11cNMWMQ-LquJb8'

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
            newMessage = message.content.split(' ', 1)[1]
            print(newMessage)
            content = newMessage.split(" ")
            name = content[0]
            dollarMessage = content[1]
            with open('data.csv', mode='a') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow([name, dollarMessage])
            calculate()
            await message.channel.send('Hello! ' + newMessage)
            
        if message.content.startswith('!calculate'):
            calculate()
        
        if message.content.startswith('!change'): 
            newMessage = message.content.split(' ', 1)[1]
            print(newMessage)
            content = newMessage.split(" ")
            row = str(content[0])
            print(row)
            dollarMessage = int(content[1])
            df = pd.read_csv('data.csv', index_col='Name')
            df2 = df.loc[row, 'Amount'] = dollarMessage
            print(df2)
            df2.to_csv('data.csv')
            calculate()
            await message.channel.send(df)

        if message.content.startswith('!delete'):
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
        
        if message.content.startswith('!total'):
            # All Function
            df = pd.read_csv('percentage.csv')
            calculate()
            await message.channel.send(df)
            # Total Function
            df = pd.read_csv("data.csv", index_col='Name') 
            totalAmount = df['Amount'].sum()
            print(totalAmount)
            await message.channel.send("Total Amount " + str(totalAmount))


    client.run(token)