import time

from mcdreforged.api.all import *

from mcdr_bot_manager.manager import *


def on_bot_sleep(server: PluginServerInterface, bot_name: str, t: int, next: str):
    time.sleep(t)
    server.dispatch_event(LiteralEvent(next), (bot_name))


def on_bot_tp(server: PluginServerInterface, bot_name: str):
    tp_bot(server, None, bot_name)


def on_bot_sp(server: PluginServerInterface, bot_name: str):
    spawn_bot(server, None, get_qbot_info(bot_name))


def on_bot_kill(server: PluginServerInterface, bot_name: str):
    kill_bot(server, bot_name)


def register(server: PluginServerInterface):
    # server.dispatch_event(LiteralEvent('my_plugin.my_event'), (1, 'a'))
    server.register_event_listener('mcdr_bot_manager.bot_sleep', on_bot_sleep)
    server.register_event_listener('mcdr_bot_manager.bot_tp', on_bot_tp)
    server.register_event_listener('mcdr_bot_manager.bot_sp', on_bot_sp)
    server.register_event_listener('mcdr_bot_manager.bot_kill', on_bot_kill)
