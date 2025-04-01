import json
from configs.map_config import MapConfig

base_dir = 'knowledge_data/firecrawl_test/sc2_unit_info/'

def process_info(unit_name):

    with open('{}{}.json'.format(base_dir, unit_name), 'r') as reader:
        info_json = json.load(reader)

    info_needed = {}
    info_needed['Unit'] = unit_name
    #info_needed['Type'] = info_json['Type']
    #info_needed['Description'] = info_json['Description']
    info_needed['Attack'] = info_json['Attack']
    info_needed['Unit stats'] = info_json['Unit stats']
    #info_needed['Strong against'] = info_json['Strong against']
    #info_needed['Weak against'] = info_json['Weak against']
    #info_needed["Competitive Usage"] = info_json["Competitive Usage"]

    return str(info_needed)

map_name = '8m'

mc = MapConfig().get_map_config(map_name)

map_config = mc['map_info']
units = mc['units_info']

units_info = ''
for a in set(units):
    units_info += process_info(a) + '\n'


unit_config = '''
The information of the units are:
{}All the units has no abilities such as blinking or equipments.
'''.format(units_info)


task_config = map_config + unit_config


prefix_code = '''
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Race, Difficulty
from sc2.ids.ability_id import AbilityId
from sc2.ids.effect_id import EffectId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
import math
import random

class MarineBot(BotAI):
'''

post_code = '''
if __name__ == '__main__':
    bot = MarineBot()
    result = run_game(maps.get('{}'), [Bot(Race.Random, bot), Computer(Race.Random, Difficulty.VeryHard)], realtime=False)
    print(result)
    print(bot.state.score.score)
    print(bot.state.score.total_damage_dealt_life)
    print(bot.state.score.total_damage_taken_life)
    print(bot.state.score.total_damage_taken_shields)
    print(len(bot.units))
    print(len(bot.enemy_units)+ len(bot.enemy_structures))
'''.format(map_name)

    
