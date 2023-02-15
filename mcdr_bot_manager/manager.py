import re

from mcdreforged.api.all import *

from mcdr_bot_manager.bot import Bot, Botinfo
from mcdr_bot_manager.text import WORLD_DICT, WORLD_NAME

bot_list: list[Bot] = []
qbot_info_list: list[Botinfo] = []
link_call_list = []


def reply(server: PluginServerInterface, info: Info, msg, q=False):
    prefix = '§6[§cMCDR-bot§6]§r '
    if q:
        prefix = '§6[§cMCDR-qbot§6]§r '
    msg = RTextList(prefix, msg)
    if info is not None:
        server.reply(info, msg)
    else:
        server.say(msg)


def get_bot(bot_name):
    for bot in bot_list:
        if bot.info.name == bot_name:
            return bot
    return None


def get_qbot_info(bot_name):
    for botinfo in qbot_info_list:
        if botinfo.name == bot_name:
            return botinfo
    return None


def print_info(server: PluginServerInterface, info: Info, binfo: Botinfo, q: bool = False):
    world = None
    if binfo.world != -1:
        world = ': ' + WORLD_DICT[WORLD_NAME[binfo.world]]
    elif binfo.pos[1] != -1:
        world = ': 跟随玩家或世界出生点'
    else:
        reply(server, info, '维度与位置: 跟随玩家或世界出生点', q)
    if world is not None:
        reply(
            server, info, '维度' + world + ' 位置 x:' + str(binfo.pos[0]) + ' y:' + str(binfo.pos[1]) +
            ' z:' + str(binfo.pos[2]), q)
    reply(server, info, 'bot备注: ' + binfo.info, q)


def info_bot(server: PluginServerInterface, info: Info, bot_name: str):
    bot = get_bot(bot_name)
    if bot:
        reply(server, info, 'Bot在线!')
        print_info(server, info, bot.info)
    else:
        reply(server, info, 'Bot未在线!')
        binfo = get_qbot_info(bot_name)
        if binfo is not None:
            reply(server, info, 'Bot快捷召唤列表信息:', True)
            print_info(server, info, binfo, True)


def tp_bot(server: PluginServerInterface,
           info: Info,
           bot_name: str,
           pos: tuple[int, int, int] = [0, 128, 0],
           world: int = 0):
    if get_bot(bot_name):
        reply(server, info, '传送中...')
        if info is not None:
            server.execute(f'execute at {info.player} run tp bot_{bot_name} {info.player}')
        else:
            server.execute(
                f'execute in minecraft:{WORLD_NAME[int(world)]} run tp bot_{bot_name} {pos[0]} {pos[1]} {pos[2]}'
            )


def spawn_bot(server: PluginServerInterface, info: Info, data: Botinfo | dict, q: bool = False):
    global bot_list
    if data is None:
        reply(server, info, 'Bot信息为空!', q)
        return
    #not quickly
    if not q:
        bot_name = 'bot_' + data[0]
        if not re.fullmatch(r'\w{1,16}', bot_name):
            reply(server, info, 'Bot名称不正确!', q)
            return
        elif kill_bot(server, data[0]):
            return
        else:
            if len(data) == 1:
                binfo = Botinfo(data[0])
            elif len(data) == 2:
                binfo = Botinfo(data[0], data[1])
            elif len(data) == 5:
                binfo = Botinfo(data[0], data[1], [data[2], data[3], data[4]])
            elif len(data) == 7:
                binfo = Botinfo(data[0], data[1], [data[2], data[3], data[4]], [data[5], data[6]])
            elif len(data) == 8:
                if data[7] in "012":
                    binfo = Botinfo(data[0], data[1], [data[2], data[3], data[4]],
                                    [data[5], data[6]], data[7])
                else:
                    reply(server, info, '世界格式不正确!', q)
                    return
            else:
                reply(server, info, '召唤参数格式不正确!', q)
                return
    #quickly
    else:
        binfo: Botinfo = data
        reply(server, info, 'bot备注: ' + binfo.info, q)
        if kill_bot(server, binfo.name):
            return
    bot_list.append(Bot(server, info, binfo))


def kill_bot(server: PluginServerInterface, bot_name: str):
    global bot_list
    bot = get_bot(bot_name)
    if not bot:
        return False
    bot.kill(server)
    bot_list.remove(bot)
    return True


def kill_all(server: PluginServerInterface):
    global bot_list
    for bot in bot_list:
        bot.kill(server)
    bot_list = []
