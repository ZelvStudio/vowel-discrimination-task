import os
import yaml
from dataclasses import dataclass, astuple

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
        self.trials = [Trial(t['index'],
                             os.path.join(self.data_path,t['file']),
                             t['vowel']) 
                       for t in self.config['Trials']]

    def __getitem__(self,n):
        return *astuple(self.trials[n]), self.vowels

    def __len__(self):
        return len(self.trials)

        
@dataclass(order=True)
class Trial:
    sort_index: int
    sound_file: str
    vowel: str
