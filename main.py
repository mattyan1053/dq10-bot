#!/usr/bin/python3
import config
import discord
from discord.ext import commands

from schedule import get_defence_schedule_string, get_guardian_schedule_string
from guardian import guardian_info
from darkness import darkness_info

TOKEN = config.DISCORD_BOT_TOKEN
intents = discord.Intents.default()
intents.typing = False

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print('ログイン完了')


# Commands
@client.command()
async def schedule(ctx, arg):
    if arg == 'defence':
        await ctx.send(get_defence_schedule_string(client))
    if arg == 'guardian':
        await ctx.send(get_guardian_schedule_string(client))
    return


@client.command()
async def guardian(ctx, arg):
    emoji_list = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
    message = ""
    if arg in guardian_info:
        jobs = guardian_info[arg]["jobs"]
        message += guardian_info[arg]["name"] + "パーティメンバー募集中\n"
        for i in range(len(jobs)):
            message += emoji_list[i] + ": " + jobs[i] + "\n"
        msg = await ctx.send(message)
        for i in range(len(jobs)):
            await msg.add_reaction(emoji_list[i])
    return


@client.command()
async def darkness(ctx, arg):
    emoji_list = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
    message = ""
    if arg in darkness_info:
        jobs = darkness_info[arg]["jobs"]
        message += darkness_info[arg]["name"] + "パーティメンバー募集中\n"
        for i in range(len(jobs)):
            message += emoji_list[i] + ": " + jobs[i] + "\n"
        msg = await ctx.send(message)
        for i in range(len(jobs)):
            await msg.add_reaction(emoji_list[i])
    return


client.run(TOKEN)
