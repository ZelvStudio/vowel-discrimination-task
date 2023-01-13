import os
import yaml
from random import sample
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
            self.config = yaml.load(f, yaml.loader.BaseLoader)
            # we use BaseLoader otherwise 'on' vowel is loaded as True
        self.vowels = self.config['Vowels']
        self.data_path = self.config['DataPath']
        self.sample_size = int(self.config['Sample'])
        self.trials = [Trial(n,
                             os.path.join(self.data_path,t['file']),
                             t['vowel']) 
                       for n,t in enumerate(self.config['Trials'])]

    def randomize(self):
        k = min(self.sample_size, len(self))
        return [t.sort_index for t in sample(self.trials,k)]

    def __getitem__(self,n):
        return *astuple(self.trials[n]), self.vowels

    def __len__(self):
        return len(self.trials)

        
@dataclass(order=True)
class Trial:
    sort_index: int
    sound_file: str
    vowel: str
