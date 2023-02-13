from mcdreforged.api.all import *

from mcdr_bot_manager.text import WORLD_NAME


class Botinfo:

    def __init__(self,
                 name: str,
                 info: str = '临时加载',
                 pos: tuple[int, int, int] = [0, -1, 0],
                 facing: tuple[int, int] = [-1, 0],
                 world: int = -1):
        self.name = name
        self.info = info
        self.pos = pos
        self.facing = facing
        self.world = world


class Bot:

    def __init__(self, server: PluginServerInterface, info: Info, Botinfo: Botinfo, qtype=False):
        self.info = Botinfo
        self.qtype = qtype
        #spawm
        if info is not None and info.is_player:
            cmd = f'execute at {info.player} run player bot_{self.info.name} spawn{self.spawn_argument()}'
        else:
            cmd = f'player bot_{self.info.name} spawn{self.spawn_argument()}'
        server.execute(cmd)

    def kill(self, server: PluginServerInterface):
        server.execute(f'player bot_{self.info.name} kill')

    def spawn_argument(self) -> str:
        temp_command: str = ''
        if self.info.pos[1] == -1:
            return temp_command
        temp_command += f' at {self.info.pos[0]} {self.info.pos[1]} {self.info.pos[2]}'
        if self.info.facing[0] == -1:
            return temp_command
        temp_command += ' facing {self.info.facing[0]} {self.info.facing[1]}'
        if self.info.world == -1:
            return temp_command
        temp_command += f' in {WORLD_NAME[int(self.info.world)]}'
        return temp_command
