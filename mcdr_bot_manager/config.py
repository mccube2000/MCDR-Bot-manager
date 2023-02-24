from mcdreforged.api.all import *

from mcdr_bot_manager.bot import Botinfo
from mcdr_bot_manager.manager import link_call_list, qbot_info_list


class NodeNameDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


keys = NodeNameDict({'data': {}})

default_config = {
    'qBotInfoList': [{
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
    }],
    'linkCall': [{
        "name": "开服加载",
        "type": "load",
        "value": "sp 1 tp 1 0 128 0 1 sleep 15 sp 1"
    }]
}

default_keys = {
    'start': '!!',
    'bot': 'bot',
    'sp': 'sp',
    'add': 'add',
    'tp': 'tp',
    'info': 'info',
    'kill': 'kill',
    'clean': 'clean',
    'call': 'call',
    'run': 'run',
    'diy': 'diy',
    'list': 'list',
    'reset': 'reset',
    'reload': 'reload',
}


def load(server: PluginServerInterface):
    global qbot_info_list
    global link_call_list

    config = server.load_config_simple('config.json', default_config)
    keys.data = NodeNameDict(server.load_config_simple('keys.json', default_keys))

    for info in config['qBotInfoList']:
        qbot_info_list.append(
            Botinfo(info['name'], info['info'], info['pos'], info['facing'], info['world']))
    for link in config['linkCall']:
        server.logger.info(str(link))
        link_call_list.append(link)


def save(server: PluginServerInterface):
    # server.save_config_simple(config,'config.json')
    server.save_config_simple(keys.data, 'keys.json')
