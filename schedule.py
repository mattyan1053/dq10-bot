from math import floor
from datetime import datetime, timedelta

# 防衛軍
def get_defence_schedule():
    standard_time = datetime(2021, 10, 31, 6, 00, 00)
    now = datetime.today()
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
    interval = (now - standard_time) / timedelta(hours=1)
    cycle = len(table)
    s = floor(((interval % cycle) + cycle) % cycle)
    table = table[s:] + table[:s] # 現在から13時間分のスケジュール
    return table


# 聖守護者
def get_guardian_schedule():
    standard_time = datetime(2021, 10, 31, 6, 00, 00)
    now = datetime.today()
    strength_map = {"purple": 0, "black": 0, "green": 1, "yellow": 1, "red": 2, "blue": 2}
    interval = (now - standard_time).days % 3
    table = {}
    for g in strength_map:
        table[g] = (strength_map[g] + interval) % 3 + 1

    return table




def get_defence_schedule_string(client):
    bouei = get_defence_schedule()

    ret = "##### 防衛軍 #####\n"
    for i in range(len(bouei)):
        ret += str((datetime.today().hour + i) % 24) + "時台: " + bouei[i] + "\n"
    return ret


def get_guardian_schedule_string(client):
    guardian = get_guardian_schedule()
    ret = "##### 聖守護者 #####\n"
    for key in guardian:
        emoji = next((emoji for emoji in client.emojis if emoji.name == "dq10_" + key), None)
        ret += "<:" + emoji.name + ":" + str(emoji.id) + ">: 強さ " + str(guardian[key]) + "\n"
    return ret
