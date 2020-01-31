import re
import csv
import discord
from dotenv import load_dotenv

def getPercentage():
    print('percentage')

class shareholder:
    def __init__(self, value):
        self.value = value
        self.name = []
        self.amountGiven = []

load_dotenv()
token = 'NjcyNjQ5NTIzMDIxMjE3Nzkz.XjOqew.TGUoyf_abVcrbWGBuB2AqQnQH74'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!create'):
        newMessage = message.content
        newMessage = message.content.split(' ', 1)[1]
        # message = newMessage.split(", ")
        # print(message)
        print(newMessage)
        dollarMessage = newMessage.split(" ")
        print(dollarMessage)

        # personOne = shareholder("personOne")
        # personOne.name.append([newMessage])
        # print(personOne.name)
        # with open('data.txt', 'w') as f:
        #     for item in personOne.name:
        #         f.write("%s\n" % item)
        await message.channel.send('Hello! ' + newMessage)
        

    
    if message.content.startswith('!change'):
        print('testing')

    if message.content.startswith('all'):
        f=open("data.txt", "r")
        if f.mode == 'r':
            contents =f.read()
            await message.channel.send(contents)

client.run(token)