from mcdr_bot_manager.text import WORLD_NAME


class Botinfo:

    def __init__(self, name, info="临时加载", pos=[None, -1, None], facing=[-1, None], world=-1):
        self.name = name
        self.info = info
        self.pos = pos
        self.facing = facing
        self.world = world


class Bot:

    def __init__(self, server, info, Botinfo, qtype=False):
        self.info = Botinfo
        self.qtype = qtype
        #spawm
        server.execute('execute at {0} run player {1} spawn{2}'.format(
            info.player, 'bot_' + self.info.name, self.spawn_argument()))

    def kill(self, server):
        #kill
        server.execute('player {0} kill'.format('bot_' + self.info.name))

    def spawn_argument(self):
        temp_command = ""
        if self.info.pos[1] == -1:
            return temp_command
        temp_command += ' at {0} {1} {2}'.format(self.info.pos[0], self.info.pos[1],
                                                 self.info.pos[2])
        if self.info.facing[0] == -1:
            return temp_command
        temp_command += ' facing {0} {1}'.format(self.info.facing[0], self.info.facing[1])
        if self.info.world == -1:
            return temp_command
        temp_command += ' in {0}'.format(WORLD_NAME[int(self.info.world)])
        return temp_command
