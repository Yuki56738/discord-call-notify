import collections
import os

import dataset
import discord

from dotenv import load_dotenv
from discord import *
from dataset import *

# https://discord.com/api/oauth2/authorize?client_id=1198563868042084352&permissions=68608&scope=bot+applications.commands

load_dotenv()
# NOTIFY_USER_ID = os.environ.get('NOTIFY_USER_ID')
# print(f'NOTIFY_USER_ID: {NOTIFY_USER_ID}')


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
    if before.channel is None and after.channel is not None:
        db = dataset.connect('sqlite:///db.sqlite')
        table: dataset.Table = db['settings']
        r: collections.OrderedDict = table.find_one(guild_id=member.guild.id)
        channel: TextChannel = member.guild.get_channel(int(r['notify_channel']))
        NOTIFY_USER_ID = os.environ.get('NOTIFY_USER_ID')
        NOTIFY_USER = await bot.fetch_user(int(NOTIFY_USER_ID))
        await channel.send(f'{NOTIFY_USER.mention} {member.name} ({member.display_name}) が参加したよ〜。')


async def checkpermit(ctx: ApplicationContext):
    if not ctx.user.id == 451028171131977738 or not ctx.user.guild_permissions.administrator:
        return False


@bot.slash_command(description='通知するチャンネルを指定する')
@commands.option(name='channelid', type=str)
async def set_notify_channel(ctx: ApplicationContext, channelid: str):
    await ctx.respond('頑張っています...')
    if not await checkpermit(ctx):
        await ctx.channel.send('権限拒否')
        return
    db = dataset.connect('sqlite:///db.sqlite')
    table: dataset.Table = db['settings']
    table.upsert({
        'notify_channel': channelid,
        'guild_id': ctx.guild.id
    }, ['id'])
    db.close()


@bot.slash_command()
@commands.option(name='user_id', type=str)
async def delusermsg(ctx: ApplicationContext, user_id: str):
    await ctx.defer()
    if not ctx.user.id == 451028171131977738:
        await ctx.send_followup('権限拒否.')
        return
    # user1 = ctx.guild.fetch_member(int(user_id))
    channels: TextChannel = await ctx.guild.fetch_channels()
    for chann in channels:
        chann: TextChannel
        try:
            msgs = await chann.history(limit=1000).flatten()
        except:
            continue
        for x in msgs:
            if x.author.id == int(user_id):
                print('deleting...')
                await ctx.send_followup('削除しています...')
                await x.delete()
    await ctx.send_followup('削除しました.')


bot.run(os.environ.get("DISCORD_TOKEN"))
