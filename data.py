import os
import yaml
from dataclasses import dataclass

# Experiment: list of Trials
#   -> can be randomized
# Trial:
#   -> file
#   -> possible vowels
#   -> truth vowel


class Experiment:
    def __init__(self,yaml_config):
        with open(yaml_config) as f:
            self.config = yaml.load(f, yaml.loader.FullLoader)
        self.vowels = self.config['Vowels']
        self.data_path = self.config['DataPath']

        
# @dataclass(order=True)
# class Trial:
#     sort_index: int
#     sound_file: str
#     vowel: str
#     possible_vowels: list = ['a','e','i','o','u','é','è','ou','an','on','in']
