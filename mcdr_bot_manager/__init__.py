# -*- coding: utf-8 -*-

from mcdreforged.api.all import *
from mcdreforged.api.utils.serializer import Serializable

import mcdr_bot_manager.command as command
import mcdr_bot_manager.event as event
from mcdr_bot_manager.bot import *
from mcdr_bot_manager.manager import *
from mcdr_bot_manager.text import GAMEMODE, HELP_MESSAGE

# def on_user_info(server: PluginServerInterface, info: Info):
#     if info.content.startswith('!!bot'):
#         info.cancel_send_to_server()
#         args = info.content.split(' ')
#         if args[0] == '!!bot':
#             del (args[0])
#             if len(args) == 0:
#                 server.reply(info, HELP_MESSAGE)
#             #bot_clean and bot_sp not exist
#             elif args[0] == 'clean' and len(args) == 1:
#                 kill_all(server)
#                 reply(server, info, 'bot已清空')
#             elif (args[0] not in ['sp', 'clean', 'kill', 'info', 'tp', 'call', 'run']
#                   and len(args) == 1) or (args[0] == 'sp' and len(args) >= 2):
#                 if args[0] == "sp":
#                     del (args[0])
#                 binfo = get_qbot_info(args[0])
#                 if binfo:
#                     spawn_bot(server, info, binfo, True)
#                 else:
#                     spawn_bot(server, info, args)
#             elif args[0] == 'kill' and len(args) == 2:
#                 if not kill_bot(server, args[1]):
#                     reply(server, info, 'Bot未在线!')
#             elif args[0] == 'info' and len(args) == 2:
#                 info_bot(server, info, args[1])
#             elif args[0] == 'tp' and len(args) == 2 and info.is_player:
#                 tp_bot(server, info, args[1])
#             elif args[0] == 'call' and len(args) >= 2:
#                 server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + args[1]), args[2:])
#             elif args[0] == 'run' and len(args) == 2:
#                 for link in link_call_list:
#                     if link['name'] == args[1]:
#                         args = link['value'].split(' ')
#                         server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + args[0]),
#                                               args[1:])
#             else:
#                 reply(server, info, '参数格式不正确!')


def on_player_joined(server: PluginServerInterface, player, info: Info):
    if get_bot(player[4:]):
        server.execute(f'gamemode {GAMEMODE} {player}')


def on_player_left(server: PluginServerInterface, message):
    bot = get_bot(message[4:])
    if bot:
        bot_list.remove(bot)


def on_load(server: PluginServerInterface, old):
    global qbot_info_list
    global link_call_list

    if old is not None:
        global bot_list
        bot_list = old.bot_list
    config = server.load_config_simple('config.json')

    for info in config["qBotInfoList"]:
        qbot_info_list.append(
            Botinfo(info['name'], info['info'], info['pos'], info['facing'], info['world']))

    for link in config["linkCall"]:
        # reply(server, None, str(link))
        server.logger.info(str(link))
        link_call_list.append(link)

    event.register(server)
    command.register(server)


def on_server_startup(server: PluginServerInterface):
    server.logger.info('运行自动bot管理......')
    for link in link_call_list:
        if link['type'] == 'load':
            args = link['value'].split(' ')
            server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + args[0]), args[1:])


def on_server_stop(server: PluginServerInterface, code):
    kill_all(server)


def on_unload(server: PluginServerInterface):
    server.logger.info('再见~')


class Config(Serializable):
    qBotInfoList: list[dict[str, int]] = {
        'name': 1,
        'info': 1,
        'pos': 1,
        'facing': 1,
        'world': 1,
    }
    linkCall: list[dict[str, int]] = {
        'name': 1,
        'type': 1,
        'value': 1,
    }
