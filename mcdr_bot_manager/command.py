from mcdreforged.api.all import *
from mcdreforged.api.command import SimpleCommandBuilder

from mcdr_bot_manager.manager import *
from mcdr_bot_manager.text import HELP_MESSAGE


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
    source.get_server().dispatch_event(LiteralEvent('mcdr_bot_manager.bot_' + args[0]), args[1:])


def __run_command(source: InfoCommandSource, args: dict):
    for link in link_call_list:
        if link['name'] == args['name']:
            __call_command(source, {'link_command': link['value']})


def register(server: PluginServerInterface):
    server.register_help_message('!!bot', 'Bot管理相关指令')
    builder = SimpleCommandBuilder()

    builder.command('!!bot', __root_command)
    # builder.command('!!bot sp', __sp_command)
    builder.command('!!bot sp <player>', __sp_command)
    builder.command('!!bot sp <player> <option>', __sp_command)
    builder.command('!!bot <player>', __q_command)
    builder.command('!!bot <player> <option>', __q_command)
    # builder.command('!!bot info', __info_command)
    builder.command('!!bot info <player>', __info_command)
    # builder.command('!!bot tp', __tp_command)
    builder.command('!!bot tp <player>', __tp_command)
    # builder.command('!!bot kill', __kill_command)
    builder.command('!!bot kill <player>', __kill_command)
    builder.command('!!bot clean', __clean_command)
    # builder.command('!!bot call', __call_command)
    builder.command('!!bot call <link_command>', __call_command)
    # builder.command('!!bot run', __run_command)
    builder.command('!!bot run <name>', __run_command)

    builder.arg('pos', Integer)
    builder.arg('player', Text)
    builder.arg('name', Text)
    builder.arg('link_command', GreedyText)
    builder.arg('option', GreedyText)

    builder.register(server)
