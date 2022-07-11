GAMEMODE = 'survival'

WORLD_NAME = ["overworld", "the_nether", "the_end"]

WORLD_DICT = {"overworld": "主世界", "the_nether": "下界", "the_end": "末地"}

HELP_MESSAGE = '''
------ MCDR Bot Manager ------
命令列表如下:
召唤一个bot:
§7!!bot sp §b<name> [<pos>] [<facing>] [0|1|2]§r
    [0]主世界,[1]下届,[2]末地.
    使用逻辑和/player spawn相同
快捷召唤bot:(可召唤快捷列表中的bot,再次输入清除.也可以召唤普通bot,但不能清除)
§7!!bot §b<name>§r
将bot添加到快捷召唤列表中:
此功能正在制作......
§7!!bot add §b<name> [<pos>] [<facing>] [0|1|2]§r
查看快捷召唤列表中的bot:
此功能正在制作......
§7!!bot list§r
查看bot信息:
§7!!bot info §b<name>§r
清除一个bot:
§7!!bot kill §b<name>§r
传送bot到您的位置:
§7!!bot tp §b<name>§r
清除所有bot:
§7!!bot clean§r
'''.strip()
