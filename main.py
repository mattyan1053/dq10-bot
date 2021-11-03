#!/usr/bin/python3
import config
import discord
from discord.ext import commands
from datetime import datetime, timedelta

from schedule import get_defence_schedule_string, get_guardian_schedule_string, get_guardian_schedule
from boss_info import boss_info

TOKEN = config.DISCORD_BOT_TOKEN


class Battle(commands.Cog):

    def __init__(self, client):
        super().__init__()
        self.client = client


    @commands.command(name="pt")
    async def pt(self, ctx, boss, date=None):
        """
        パーティ募集

        boss: 募集したいボスのタグ
        date(Optional): 日付(format yyyy-mm-dd)
        """
        try:
            if date is None:
                date = datetime.today() - timedelta(hours=6) # 0:00~5:59までは前日扱い
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
                if date < datetime.today():
                    await ctx.send("過去の日付は指定できません")
                    return
        except:
            await ctx.send("dateのフォーマットが違います。")
            return
        date = date.replace(hour=6, minute=0,second=0, microsecond=0) # その日の6時に設定する

        if boss in boss_info:
            emoji_list = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"]
            message = "### パーティ募集中 (" + date.strftime("%Y-%m-%d") +  ") ###\n"
            jobs = boss_info[boss]["jobs"]
            message += boss_info[boss]["name"]
            guardian_table, standard_time = get_guardian_schedule(date)
            if guardian_table is None:
                return
            # 聖守護者の場合、強さ表示
            if boss in guardian_table:
                # 絵文字のkeyはハイフンが使えないのでアンダースコアに。
                emoji = next((emoji for emoji in self.client.emojis if emoji.name == "dq10_" + boss.replace('-', '_')), None)
                message += "<:" + emoji.name + ":" + str(emoji.id) + ">: 強さ " + str(guardian_table[boss]) + "\n"

            for i, value in enumerate(jobs):
                message += emoji_list[i] + ": " + value + "\n"
            slime = next((emoji for emoji in self.client.emojis if emoji.name == "slime"), None)
            message += "<:" + slime.name + ":" + str(slime.id) + ">: なんでも可\n"
            msg = await ctx.send(message)
            for i in range(len(jobs)):
                await msg.add_reaction(emoji_list[i])
            await msg.add_reaction(slime)
            await msg.pin()
        else:
            ctx.send("ボス名が不正です。")
            return
        return


    @commands.command(name="sc")
    async def schedule(self, ctx, kind, date=None):
        """
        つよさ予報

        kind: d=防衛軍, g=聖守護者
        date(Optional): 日付(format yyyy-mm-dd)
        """
        try:
            if date is None:
                date = datetime.today() - timedelta(hours=6) # 0:00~5:59までは前日扱い
            else:
                date = datetime.strptime(date, "%Y-%m-%d")
        except:
            await ctx.send("dateのフォーマットが違います。")
            return
        date = date.replace(hour=6, minute=0,second=0, microsecond=0) # その日の6時に設定する

        if kind == "d":
            await ctx.send(get_defence_schedule_string(self.client, date))
            return
        if kind == "g":
            await ctx.send(get_guardian_schedule_string(self.client, date))
            return

        ctx.send("kindが不正です。")
        return


    @commands.command(name="list")
    async def _list(self, ctx):
        """
        ボス一覧
        """
        message = "[tag] ボス名 \n========================\n"
        for boss in boss_info:
            message += "[" + boss + "] " + boss_info[boss]["name"] + "\n"
        await ctx.send(message)
        return


intents = discord.Intents.default()
intents.typing = False
client = commands.Bot(command_prefix='/', intents=intents)
client.add_cog(Battle(client=client))
client.run(TOKEN)
