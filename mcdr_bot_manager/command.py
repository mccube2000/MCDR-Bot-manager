from mcdreforged.api.all import *
from mcdreforged.api.command import SimpleCommandBuilder

from mcdr_bot_manager.event import call_next
from mcdr_bot_manager.manager import *
from mcdr_bot_manager.text import HELP_MESSAGE


class NodeNameDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


# command keys
ck: NodeNameDict


def __root_command(source: InfoCommandSource):
    source.reply(HELP_MESSAGE)


def __clean_command(source: InfoCommandSource):
    kill_all(source.get_server())
    source.reply('bot已清空')


def __info_command(source: InfoCommandSource, args: dict):
    info_bot(source.get_server(), source.get_info(), args['player'])


def __tp_command(source: InfoCommandSource, args: dict):
    if source.is_player:
        tp_bot(source.get_server(), source.get_info(), args['player'])
    else:
        source.reply('非玩家不能使用tp指令')


def __kill_command(source: InfoCommandSource, args: dict):
    if not kill_bot(source.get_server(), args['player']):
        source.reply('Bot未在线!')


def __q_command(source: InfoCommandSource, args: dict, is_sp: bool = False):
    server = source.get_server()
    info = source.get_info()
    option = []
    if 'option' in args:
        option = args['option'].split()
    player = args['player']
    binfo = get_qbot_info(player)
    if binfo:
        spawn_bot(server, info, binfo, True)
    else:
        spawn_bot(server, info, [player, *option])


def __sp_command(source: InfoCommandSource, args: dict):
    __q_command(source, args, True)


def __call_command(source: InfoCommandSource, args: dict):
    args = args['link_command'].split(' ')
    if len(args) > 1:
        call_next(source.get_server(), args[0], args[1:])
    else:
        source.reply('链式命令格式错误!')


def __run_command(source: InfoCommandSource, args: dict):
    for link in link_call_list:
        if link['name'] == args['name']:
            __call_command(source, {'link_command': link['value']})


def __ch_key(source: InfoCommandSource, name: str, new_name: str, reset: bool = False):
    key = ''
    for k, v in ck.items():
        if v == name:
            key = k
    if key == '':
        source.reply(f'关键字 {name} 不存在!')
    else:
        if reset:
            new_name = key
            if new_name == 'start':
                new_name = '!!'
            ck[key] = new_name
            source.reply(f'关键字 {name} 已重置为 {new_name} 重载插件生效!')
        else:
            ck[key] = new_name
            source.reply(f'关键字 {name} 已修改为 {new_name} 重载插件生效!')


def __diy_command(source: InfoCommandSource, args: dict):
    name = args['name']
    if 'new_name' in args:
        __ch_key(source, name, args['new_name'])
    else:
        __ch_key(source, name, None, True)


def register(server: PluginServerInterface, keys: dict):
    global ck
    ck = NodeNameDict(keys)
    root = ck.start + ck.bot

    server.register_help_message(root, 'Bot管理相关指令')
    builder = SimpleCommandBuilder()
    builder.command(f'{root}', __root_command)
    # builder.command(f'{root} {ck.sp}', __sp_command)
    builder.command(f'{root} {ck.sp} <player>', __sp_command)
    builder.command(f'{root} {ck.sp} <player> <option>', __sp_command)
    # builder.command(f'{root} {ck.info}', __info_command)
    # builder.command(f'{root} {ck.info} {ck.list}', __info_command)
    builder.command(f'{root} {ck.info} <player>', __info_command)
    # builder.command(f'{root} {ck.tp}', __tp_command)
    builder.command(f'{root} {ck.tp} <player>', __tp_command)
    # builder.command(f'{root} {ck.kill}', __kill_command)
    builder.command(f'{root} {ck.kill} <player>', __kill_command)
    builder.command(f'{root} {ck.clean}', __clean_command)
    # builder.command(f'{root} {ck.call}', __call_command)
    # builder.command(f'{root} {ck.call} {ck.list}', __call_command)
    builder.command(f'{root} {ck.call} <link_command>', __call_command)
    # builder.command(f'{root} {ck.run}', __run_command)
    # builder.command(f'{root} {ck.run} {ck.list}', __run_command)
    builder.command(f'{root} {ck.run} <name>', __run_command)
    # builder.command(f'{root} {ck.diy} {ck.list}', __diy_command)
    builder.command(f'{root} {ck.diy} {ck.reset} <name>', __diy_command)
    builder.command(f'{root} {ck.diy} <name> <new_name>', __diy_command)
    builder.command(f'{root} <player>', __q_command)
    builder.command(f'{root} <player> <option>', __q_command)

    builder.arg('pos', Integer)
    builder.arg('player', Text)
    builder.arg('name', Text)
    builder.arg('new_name', Text)
    builder.arg('link_command', GreedyText)
    builder.arg('option', GreedyText)

    builder.register(server)
