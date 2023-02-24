# -*- coding: utf-8 -*-
from mcdreforged.api.all import *

import mcdr_bot_manager.command as command
import mcdr_bot_manager.config as config
import mcdr_bot_manager.event as event
from mcdr_bot_manager.manager import (bot_list, get_bot, kill_all, link_call_list)
from mcdr_bot_manager.text import GAMEMODE


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
        for bot in old.manager.bot_list:
            bot_list.append(bot)
    config.load(server)
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
    config.save(server)
    server.logger.info('再见~')
