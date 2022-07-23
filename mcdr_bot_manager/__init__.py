# -*- coding: utf-8 -*-
import json

from mcdreforged.api.all import *

from mcdr_bot_manager.bot import *
from mcdr_bot_manager.event import register
from mcdr_bot_manager.manager import *
from mcdr_bot_manager.text import GAMEMODE, HELP_MESSAGE

# def on_unload(server: PluginServerInterface):
#     server.logger.info('Bye')

# def on_server_startup(server: PluginServerInterface):
#     server.logger.info('Server has started')


def on_user_info(server: PluginServerInterface, info: Info):
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
            elif (args[0] not in ['sp', 'clean', 'kill', 'info', 'tp', 'call']
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
                info_bot(server, info, args[1])
            elif args[0] == 'tp' and len(args) == 2 and info.is_player:
                tp_bot(server, info, args[1])
            elif args[0] == 'call' and len(args) >= 2:
                reply(server, info, 'call: ' + args[1])
                tu = (args[2])
                if args[1] == 'sleep':
                    tu = (args[2], args[3], args[4])
                server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + args[1]), tu)
            else:
                reply(server, info, '参数格式不正确!')


def on_player_joined(server: PluginServerInterface, player, info: Info):
    if get_bot(player[4:]):
        server.execute(f'gamemode {GAMEMODE} {player}')


def on_player_left(server: PluginServerInterface, message):
    bot = get_bot(message[4:])
    if bot:
        bot_list.remove(bot)


def on_load(server: PluginServerInterface, old):
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
    register(server)


def on_server_stop(server: PluginServerInterface, code):
    kill_all()


# def register(server: PluginServerInterface):
# server.register_command(
#     Literal('!!cexample').runs(lambda src: src.reply('Hello world from sample command')))
# server.register_help_message('!!example', 'Hello world')
# server.register_help_message('!!cexample', 'Hello world from command')
