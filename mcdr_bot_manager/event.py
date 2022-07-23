import time

from mcdreforged.api.all import *

from mcdr_bot_manager.manager import *


def on_bot_sleep(server: PluginServerInterface, t: int, next: str = None, *args):
    reply(server, None, f'暂停 {t}s, 下一步: {next} 参数: {args}', True)
    time.sleep(int(t))
    if next is not None:
        server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + next), args)


def on_bot_tp(server: PluginServerInterface,
              bot_name: str,
              x: int,
              y: int,
              z: int,
              world: int,
              next: str = None,
              *args):
    reply(server, None, f'传送 bot_{bot_name} 到 {WORLD_DICT[WORLD_NAME[int(world)]]} [{x},{y},{z}]',
          True)
    tp_bot(server, None, bot_name, (x, y, z), world)
    if next is not None:
        server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + next), args)


def on_bot_sp(server: PluginServerInterface, bot_name: str, next: str = None, *args):
    reply(server, None, f'召唤/杀死 bot_{bot_name} ', True)
    spawn_bot(server, None, get_qbot_info(bot_name), True)
    if next is not None:
        server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + next), args)


def on_bot_kill(server: PluginServerInterface, bot_name: str, next: str = None, *args):
    reply(server, None, f'杀死 bot_{bot_name} ', True)
    kill_bot(server, bot_name)
    if next is not None:
        server.dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + next), args)


def register(server: PluginServerInterface):
    # server.dispatch_event(LiteralEvent('my_plugin.my_event'), (1, 'a'))
    server.register_event_listener('mcdr_bot_manager.bot_sleep', on_bot_sleep)
    server.register_event_listener('mcdr_bot_manager.bot_tp', on_bot_tp)
    server.register_event_listener('mcdr_bot_manager.bot_sp', on_bot_sp)
    server.register_event_listener('mcdr_bot_manager.bot_kill', on_bot_kill)
