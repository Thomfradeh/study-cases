import Study_Case_1 as sc_i
from math import log10

class Entity():
    attributes = ('STR', 'DEX', 'VIT', 'PER', 'INT', 'CHA', 'LCK', 'WIS', 'ARC', 'PAT')
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties include:
         - name
         - attr_values
         - attr_die
         
         Current methods include:
         - Builder patter for every property
         - roll_stat: Interaction facilitator, returns the power level of a roll
         """
        self.name = ''
        self.attr_values = {
            'STR': 1,
            'DEX': 1,
            'VIT': 1,
            'PER': 1,
            'INT': 1,
            'CHA': 1,
            'LCK': 1,
            'WIS': 1,
            'ARC': 1,
            'PAT': 1
        }
        self.attr_die = {
            'STR': None,
            'DEX': None,
            'VIT': None,
            'PER': None,
            'INT': None,
            'CHA': None,
            'LCK': None,
            'WIS': None,
            'ARC': None,
            'PAT': None
        }
    
    def set_attribute(self, attribute: str, value: int):
        """Builder pattern for attr_values.
        
        The attribute names are as follows:
         - STR: Strength
         - DEX: Dexterity
         - VIT: Vitality
         - PER: Perception
         - INT: Inteligence
         - CHA: Charisma
         - LCK: Luck
         - WIS: Wisdom
         - ARC: Arcane
         - PAT: Patience
         """
        if attribute.upper() not in self.attributes:
            raise ValueError('Invalid Attribute')
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        "Builder pattern for name"
        self.name = name
        return self
    

    def battle_stats(self):
        """Engagement Stats Generator. Returns a List with the following:
        
        - Given Entity
        - Entity's HP: calculate through: 5**log10(VIT) * log10(VIT)*2
        """

        log_vit = log10(self.attr_values['VIT'])
        health_points = int(5**log_vit * log_vit*2)

        return (self, health_points)

    
    @classmethod
    def roll_stat(cls, char, attribute: str, scale: int = 0.1):
        "Rolls a given stat for a given character, according to it's corresponding dice (defaults to d20)."
        if attribute.upper() not in cls.attributes:
            raise ValueError('Invalid Attribute')
        
        dice = char.attr_die[attribute.upper()]
        if dice is None:
            dice = sc_i.Dice().set_num_sides(20)
        
        modifier = sc_i.Dice.roll(dice) * scale
        return char.attr_values[attribute.upper()] * (modifier+0.4)
    

class Game_Master():
    def __init__(self) -> None:
        self.active_entities = {}

    def add_entities(self, ent_list: tuple):
        for entity in ent_list:
            if type(entity) is not Entity:
                raise TypeError('Entity list contains non-entity elements')
            
            battle_stats = entity.battle_stats()
            self.active_entities[battle_stats[0]] = (battle_stats[1])

    @classmethod
    def clash_stats(cls, entity_1: Entity, stat_1:str, entity_2:Entity, stat_2:str):
        if type(entity_1) is not Entity or type(entity_2) is not Entity:
            raise TypeError('Non-entity element passed as entity')

        roll_1 = Entity.roll_stat(entity_1, stat_1)
        roll_2 = Entity.roll_stat(entity_2, stat_2)

        if roll_1 > roll_2:
            return (0, roll_1)
        return (1, roll_2)

    @classmethod
    def delta_HP(cls, entity, damage):
        pass
        

dave = Entity().set_attribute('Vit', 3156)
joe = Entity().set_attribute('Str', 2865)

game = Game_Master()
game.add_entities([dave, joe])

print(game.clash_stats(dave, 'Vit', joe, 'Str'))
