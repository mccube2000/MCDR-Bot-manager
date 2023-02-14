# -*- coding: utf-8 -*-

from mcdreforged.api.all import *
from mcdreforged.api.utils.serializer import Serializable

import mcdr_bot_manager.command as command
import mcdr_bot_manager.event as event
from mcdr_bot_manager.bot import *
from mcdr_bot_manager.manager import *
from mcdr_bot_manager.text import GAMEMODE


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

    config = server.load_config_simple('config.json', target_class=Config)
    keys = server.load_config_simple('keys.json', target_class=Keys)

    for info in config.qBotInfoList:
        qbot_info_list.append(
            Botinfo(info['name'], info['info'], info['pos'], info['facing'], info['world']))
    for link in config.linkCall:
        server.logger.info(str(link))
        link_call_list.append(link)

    event.register(server)
    command.register(server, keys.keys)


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
    qBotInfoList: list[dict] = [{
        "name": "1",
        "info": "跟随玩家召唤",
        "pos": [0, -1, 0],
        "facing": [-1, 0],
        "world": -1
    }, {
        "name": "2",
        "info": "地狱加载",
        "pos": [0, 100, 0],
        "facing": [0, 0],
        "world": 1
    }, {
        "name": "3",
        "info": "末地加载",
        "pos": [0, 100, 0],
        "facing": [0, 0],
        "world": 2
    }]
    linkCall: list[dict] = [{
        "name": "开服加载",
        "type": "load",
        "value": "sp 1 tp 1 0 128 0 1 sleep 15 sp 1"
    }]


class Keys(Serializable):
    keys: dict = {
        'start': '!!',
        'bot': 'bot',
        'sp': 'sp',
        'tp': 'tp',
        'info': 'info',
        'kill': 'kill',
        'clean': 'clean',
        'call': 'call',
        'run': 'run',
        'diy': 'diy',
        'list': 'list',
        'reset': 'reset',
    }
