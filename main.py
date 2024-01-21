import os
import discord
from dotenv import load_dotenv
from discord import *

# https://discord.com/api/oauth2/authorize?client_id=1198563868042084352&permissions=68608&scope=bot+applications.commands

load_dotenv()

bot = discord.Bot(intentes=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user}')
    print('Connected to following guilds:')
    for x in bot.guilds:
        print(x.name)
    print('--------------------')
@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    pass

bot.run(os.environ.get("DISCORD_TOKEN"))