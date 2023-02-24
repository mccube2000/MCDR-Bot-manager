from mcdreforged.api.all import *
from mcdreforged.api.command import SimpleCommandBuilder

from mcdr_bot_manager.config import NodeNameDict, keys
from mcdr_bot_manager.event import call_next
from mcdr_bot_manager.manager import *

info: NodeNameDict


def reply(source: CommandSource, msg, q=False):
    prefix = '§6[§cMCDR-bot§6]§r '
    if q:
        prefix = '§6[§cMCDR-qbot§6]§r '
    msg = RTextList(prefix, msg)
    if source.is_player:
        source.get_server().say(msg)
    else:
        source.reply(msg)


def __root_command(source: InfoCommandSource):
    msg = RTextList('§6------ §cMCDR Bot Manager§6 ------§r\n', '§c< >§r为必需填写的参数\n',
                    '§6[ ]§r为可选填写的参数\n', '命令列表如下:\n', *info.sp, *info.quick, *info.add, *info.list,
                    *info.info, *info.kill, *info.clean, *info.tp, *info.call, *info.run, *info.diy)
    source.reply(msg)


def __clean_command(source: InfoCommandSource):
    kill_all(source.get_server())
    source.reply('bot已清空')


def __list_command(source: InfoCommandSource, args: dict):
    ...


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


def __q_command(source: InfoCommandSource, args: dict, q: bool = True):
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
    __q_command(source, args, False)


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


def __ch_key(source: InfoCommandSource, name: str, new_name: str):
    key = ''
    for k, v in keys.data.items():
        if v == name:
            key = k
    if key == '':
        source.reply(f'关键字 {name} 不存在!')
    else:
        if new_name is None:
            new_name = key
            if new_name == 'start':
                new_name = '!!'
            keys.data[key] = new_name
            source.reply(f'关键字 {name} 已重置为 {new_name} 重载插件生效!')
        else:
            keys.data[key] = new_name
            source.reply(f'关键字 {name} 已修改为 {new_name} 重载插件生效!')


def __diy_command(source: InfoCommandSource, args: dict):
    key = args['key']
    if 'new_key' in args:
        __ch_key(source, key, args['new_key'])
    else:
        __ch_key(source, key, None)


def register(server: PluginServerInterface):
    global info
    ck: NodeNameDict = keys.data
    root = ck.start + ck.bot
    builder = SimpleCommandBuilder()

    # root
    info = NodeNameDict(
        {'root': [RText('§lBot管理相关指令§r').h('点击执行命令').c(RAction.run_command, f'{root}')]})
    server.register_help_message(root, RTextList(*info.root))
    builder.command(f'{root}', __root_command)

    # sp
    info.sp = [
        '§6*§l召唤一个bot:§r(使用逻辑和/player spawn相同)\n',
        RText(f'§7{root} {ck.sp} §c<name> §6[info] [pos] [facing] [0|1|2]§r\n').h('点击输入命令').c(
            RAction.suggest_command, f'{root} {ck.sp} 名称 信息 x y z 朝向0 朝向1 维度'),
        '    §6[0]§r主世界 §6[1]§r下届 §6[2]§r末地\n'
    ]
    builder.command(f'{root} {ck.sp}', lambda s: s.reply(RTextList(*info.sp)))
    builder.command(f'{root} {ck.sp} <player>', __sp_command)
    builder.command(f'{root} {ck.sp} <player> <option>', __sp_command)

    # add
    info.add = [
        f'*§l将bot添加到快捷召唤列表中:§r(和§7{root} {ck.sp}§r相似)\n',
        RText(f'§7{root} {ck.add} §c<name> §6[info] [pos] [facing] [0|1|2]§r\n').h('点击输入命令').c(
            RAction.suggest_command, f'{root} {ck.add} 名称 信息 x y z 朝向0 朝向1 维度')
    ]
    builder.command(f'{root} {ck.add}', lambda s: s.reply(RTextList(*info.add)))
    # builder.command(f'{root} {ck.add} <player>', __sp_command)  # *
    # builder.command(f'{root} {ck.add} <player> <option>', __sp_command)  # *

    # list
    info.list = [
        '*§l查看快捷召唤列表中的bot:§r\n',
        RText(f'§7{root} {ck.list}\n').h('点击执行命令').c(RAction.run_command, f'{root} {ck.list}')
    ]
    # builder.command(f'{root} {ck.list}', __list_command)

    # info
    info.info = [
        '§6*§l查看bot信息:§r\n',
        RText(f'§7{root} {ck.info} §c<name>\n').h('点击输入命令').c(RAction.suggest_command,
                                                              f'{root} {ck.info} 名称')
    ]
    builder.command(f'{root} {ck.info}', lambda s: s.reply(RTextList(*info.info)))
    builder.command(f'{root} {ck.info} <player>', __info_command)

    # kill
    info.kill = [
        '§6*§l清除一个bot:§r\n',
        RText(f'§7{root} {ck.kill} §c<name>\n').h('点击输入命令').c(RAction.suggest_command,
                                                              f'{root} {ck.kill} 名称')
    ]
    builder.command(f'{root} {ck.kill}', lambda s: s.reply(RTextList(*info.kill)))
    builder.command(f'{root} {ck.kill} <player>', __kill_command)

    # clean
    info.clean = [
        '§6*§l清除所有bot:§r\n',
        RText(f'§7{root} {ck.clean}\n').h('点击输入命令').c(RAction.suggest_command, f'{root} {ck.clean}')
    ]
    builder.command(f'{root} {ck.clean}', __clean_command)

    # tp
    info.tp = [
        '§6*§l传送bot到您的位置:§r\n',
        RText(f'§7{root} {ck.tp} §c<name>\n').h('点击输入命令').c(RAction.suggest_command,
                                                            f'{root} {ck.tp} 名称')
    ]
    builder.command(f'{root} {ck.tp}', lambda s: s.reply(RTextList(*info.tp)))
    builder.command(f'{root} {ck.tp} <player>', __tp_command)

    # call
    info.call = [
        '§6*§l执行链式命令:§r\n',
        RText(f'§7{root} {ck.call} §c<link_command>\n').h('点击输入命令').c(RAction.suggest_command,
                                                                      f'{root} {ck.call} 命令...')
    ]
    builder.command(f'{root} {ck.call}', lambda s: s.reply(RTextList(*info.call)))
    # builder.command(f'{root} {ck.call} {ck.list}', __call_command)  # *
    builder.command(f'{root} {ck.call} <link_command>', __call_command)

    # run
    info.run = [
        '§6*§l执行配置文件中的链式命令:§r\n',
        RText(f'§7{root} {ck.run} §c<name>\n').h('点击输入命令').c(RAction.suggest_command,
                                                             f'{root} {ck.run} 名称')
    ]
    builder.command(f'{root} {ck.run}', lambda s: s.reply(RTextList(*info.run)))
    # builder.command(f'{root} {ck.run} {ck.list}', __run_command)  # *
    builder.command(f'{root} {ck.run} <name>', __run_command)

    # diy
    info.diy = [
        '*§l查看关键字列表:§r(关键字是命令中的§7灰色§r部分，包括§7!!§r)\n',
        RText(f'§7{root} {ck.diy} {ck.list}\n').h('点击执行命令').c(RAction.run_command,
                                                              f'{root} {ck.diy} {ck.list}'),
        '§6*§l重置现有关键字为默认值:§r\n',
        RText(f'§7{root} {ck.diy} {ck.reset} §c<key>\n').h('点击输入命令').c(
            RAction.suggest_command, f'{root} {ck.diy} {ck.reset} 关键字'), '§6*§l执行配置文件中的链式命令:§r\n',
        RText(f'§7{root} {ck.diy} §c<key> <new_key>\n').h('点击输入命令').c(RAction.suggest_command,
                                                                      f'{root} {ck.diy} 关键字 新关键字')
    ]
    builder.command(f'{root} {ck.diy}', lambda s: s.reply(RTextList(*info.diy)))
    # builder.command(f'{root} {ck.diy} {ck.list}', __diy_command)  # *
    builder.command(f'{root} {ck.diy} {ck.reset} <key>', __diy_command)
    builder.command(f'{root} {ck.diy} <key> <new_key>', __diy_command)

    # reload
    info.reload = [
        '§6*§l重载插件并重载配置文件:§r\n',
        RText(f'§7{root} {ck.reload} §c<name>\n').h('点击输入命令').c(RAction.suggest_command,
                                                                f'{root} {ck.reload}')
    ]
    builder.command(f'{root} {ck.reload}',
                    lambda s: s.get_server().reload_plugin("mcdr_bot_manager"))

    # quick
    info.quick = [
        '§6*§l快捷召唤bot:§r(可召唤快捷列表中的bot, 再次输入清除. 也可以召唤/清除普通bot)\n',
        RText(f'§7{root} §c<name>§r\n').h('点击输入命令').c(RAction.suggest_command, f'{root} 名称')
    ]
    builder.command(f'{root} <player>', __q_command)

    builder.arg('pos', Integer)
    builder.arg('player', Text)
    builder.arg('name', Text)
    builder.arg('key', Text)
    builder.arg('new_key', Text)
    builder.arg('link_command', GreedyText)
    builder.arg('option', GreedyText)

    builder.register(server)
