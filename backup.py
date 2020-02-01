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


def Convert(dollarMessage): 
    res_dct = {dollarMessage[i]: dollarMessage[i + 1] for i in range(0, len(dollarMessage), 2)} 
    return res_dct 

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
        print(newMessage)
        dollarMessage = newMessage.split(" ")
        print(Convert(dollarMessage))
        my_dict = Convert(dollarMessage)
        with open('test.csv', 'a') as f:
            for key in my_dict.keys():
                f.write("%s,%s\n"%(key,my_dict[key]))
        # personOne = shareholder("personOne")
        # personOne.name.append([newMessage])
        # print(personOne.name)
        with open('data.txt', 'a+') as f:
            for key in my_dict.keys():
                f.write("%s,%s\n"%(key,my_dict[key]))
        
        await message.channel.send('Hello! ' + newMessage)
        
    if message.content.startswith('!calculate'):
        f=open("test.csv", "r")
        if f.mode == 'r':
            print('testing')
            
    
    if message.content.startswith('!change'):
        print('testing')

    if message.content.startswith('all'):
        f=open("test.csv", "r")
        if f.mode == 'r':
            contents =f.read()
            await message.channel.send(contents)

client.run(token)