from math import floor
from datetime import datetime, timedelta


# 防衛軍
def get_defence_schedule_string(client, date):
    table, standard_time = get_defence_schedule(date)
    if table is None:
        return standard_time.strftime("%Y-%m-%d") + "以前のつよさ予報は未対応です。"

    ret = "##### 防衛軍 (" + date.strftime("%Y-%m-%d") + ") #####\n"
    table = (table + table)[:24] # 24時間分のテーブルに変換
    for i, enemy in enumerate(table):
        ret += str((i + 6) % 24) + "時台: " + enemy + "\n"
    return ret


def get_defence_schedule(date):
    standard_time = datetime(2021, 10, 31, 6, 00, 00)
    if date < standard_time:
        return None, standard_time
    table = [
        '闇朱の獣牙兵団',
        '紫炎の鉄機兵団',
        '彩虹の粘塊兵団',
        '    全兵団   ',
        '新碧の造魔兵団',
        '蒼怨の屍獄兵団',
        '銀甲の凶蟲兵団',
        '彩虹の粘塊兵団',
        '    全兵団   ',
        '翠煙の海妖兵団',
        '灰塵の竜鱗兵団',
        '彩虹の粘塊兵団',
        '    全兵団   '
    ]
    interval = (date - standard_time) / timedelta(hours=1)
    cycle = len(table)
    s = floor(((interval % cycle) + cycle) % cycle)
    table = table[s:] + table[:s] # 現在からlen(table)時間分のスケジュール
    return table, standard_time


# 聖守護者
def get_guardian_schedule_string(client, date):
    table, standard_time = get_guardian_schedule(date)
    if table is None:
        return standard_time.strftime("%Y-%m-%d") + "以前のつよさ予報は未対応です。"
    ret = "##### 聖守護者 (" + date.strftime("%Y-%m-%d") + ") #####\n"
    for key in table:
        emoji = next((emoji for emoji in client.emojis if emoji.name == "dq10_" + key.replace('-', '_')), None)
        ret += "<:" + emoji.name + ":" + str(emoji.id) + ">: 強さ " + str(table[key]) + "\n"
    return ret


def get_guardian_schedule(date):
    standard_time = datetime(2021, 10, 31, 6, 00, 00)
    if date < standard_time:
        return None, standard_time
    strength_map = {"g-purple": 0, "g-black": 0, "g-green": 1, "g-yellow": 1, "g-red": 2, "g-blue": 2}
    interval = (date - standard_time).days % 3
    table = {}
    for g in strength_map:
        table[g] = (strength_map[g] + interval) % 3 + 1

    return table, standard_time
