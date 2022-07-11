# -*- coding: utf-8 -*-
import json
import os
import re

from mcdreforged.api.all import *

from mcdr_bot_manager.bot import *
from mcdr_bot_manager.text import GAMEMODE, HELP_MESSAGE, WORLD_DICT


def on_unload(server: PluginServerInterface):
    server.logger.info('Bye')


def on_server_startup(server: PluginServerInterface):
    server.logger.info('Server has started')


ConfigFilePath = os.path.join('config', 'MCDR-bot-manager.json')

bot_list = []
qbot_info_list = []


def reply(server, info, msg, q=False):
    if q:
        server.reply(info, '[MCDR-qbot] ' + msg)
    else:
        server.reply(info, '[MCDR-bot] ' + msg)


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


def spawn_bot(server, info, data, q=False):
    global bot_list
    #not quickly
    if not q:
        bot_name = 'bot_' + data[0]
        if not re.fullmatch(r'\w{1,16}', bot_name):
            reply(server, info, 'Bot名称不正确!', q)
            return
        elif get_bot(data[0]):
            reply(server, info, 'Bot已经在线!', q)
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
        binfo = data
        reply(server, info, 'bot备注: ' + binfo.info, q)
        bot = get_bot(binfo.name)
        if bot:
            kill_bot(server, binfo.name)
            bot_list.remove(bot)
            return
    bot_list.append(Bot(server, info, binfo))


def kill_bot(server, bot_name):
    global bot_list
    bot = get_bot(bot_name)
    if not bot:
        return False
    bot.kill(server)
    bot_list.remove(bot)
    return True


def kill_all(server):
    global bot_list
    for bot in bot_list:
        bot.kill(server)
    bot_list = []


def on_user_info(server, info):
    if info.content.startswith('!!bot'):
        info.cancel_send_to_server()
        args = info.content.split(' ')
        global bot_list
        global qbot_info_list
        if args[0] == '!!bot':
            del (args[0])
            if len(args) == 0:
                server.reply(info, HELP_MESSAGE)
            #bot_clean and bot_sp not exist
            elif args[0] == 'clean' and len(args) == 1:
                kill_all(server)
                reply(server, info, 'bot已清空')
            elif (args[0] not in ['sp', 'clean', 'kill', 'info', 'tp']
                  and len(args) == 1) or (args[0] == 'sp' and len(args) >= 2):
                if args[0] == "sp":
                    del (args[0])
                binfo = get_qbot_info(args[0])
                if binfo:
                    spawn_bot(server, info, binfo, True)
                else:
                    spawn_bot(server, info, args)
            elif args[0] == 'kill' and len(args) == 2:
                if not kill_bot(server, args[1]):
                    reply(server, info, 'Bot未在线!')
            elif args[0] == 'info' and len(args) == 2:
                binfo = get_qbot_info(args[1])
                bot = get_bot(args[1])
                if bot:
                    if bot.info.pos[1] != -1:
                        reply(
                            server, info, '位于: ' + WORLD_DICT[WORLD_NAME[0]] + 'x' +
                            bot.info.pos[0] + ' y' + bot.info.pos[1] + ' z' + bot.info.pos[2], True)
                    if bot.info.world != -1:
                        reply(
                            server, info, '位于: ' + WORLD_DICT[WORLD_NAME[bot.info.world]] + 'x' +
                            bot.info.pos[0] + ' y' + bot.info.pos[1] + ' z' + bot.info.pos[2], True)
                    reply(server, info, 'bot备注: ' + bot.info.info)
                else:
                    reply(server, info, 'Bot未在线!')
                    if binfo:
                        reply(server, info, 'Bot位于快捷召唤列表', True)
                        reply(
                            server, info, '位置: ' + WORLD_DICT[WORLD_NAME[binfo.world]] + ' x' +
                            str(binfo.pos[0]) + ' y' + str(binfo.pos[1]) + ' z' + str(binfo.pos[2]),
                            True)
                        reply(server, info, 'bot备注: ' + binfo.info, True)
            elif args[0] == 'tp' and len(args) == 2 and info.is_player:
                bot_name = args[2]
                if get_bot(bot_name):
                    reply(server, info, '传送中...')
                    server.execute('execute at {0} run tp {1} {0}'.format(
                        info.player, 'bot_' + bot_name))
            else:
                reply(server, info, '参数格式不正确!')


def on_player_joined(server, player, info):
    if get_bot(player[4:]):
        server.execute('gamemode {} {}'.format(GAMEMODE, player))


def on_player_left(server, message):
    bot = get_bot(message[4:])
    if bot:
        bot_list.remove(bot)


def on_load(server, old):
    if old is not None:
        global bot_list
        bot_list = old.bot_list

    global qbot_info_list
    with open(ConfigFilePath, 'r') as f:
        js = json.load(f)
        blist = js["qBotInfoList"]
        for info in blist:
            qbot_info_list.append(Botinfo(info[0], info[1], info[2], info[3], info[4]))

    server.register_help_message('!!bot', 'Bot相关指令')
    # register(server)


def on_server_stop(server, code):
    kill_all()


# def register(server: PluginServerInterface):
#     server.register_command(
#         Literal('!!cexample').runs(lambda src: src.reply('Hello world from sample command')))
#     server.register_help_message('!!example', 'Hello world')
#     server.register_help_message('!!cexample', 'Hello world from command')