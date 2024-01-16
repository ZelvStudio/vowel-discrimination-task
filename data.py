import os
import yaml
import re
from random import sample
from dataclasses import dataclass, astuple

# Experiment: list of Trials
#   -> can be randomized
# Trial:
#   -> file
#   -> possible vowels
#   -> truth vowel

def _get_assist(filename: str) -> float:
    """ get assist value from vowel filename
        example: a_003_sync_1_assist_08.short.wav -> match '08'
                                                  -> floatable '0.8'
                                                  -> return 0.8
    """
    assist_regex = re.compile(r'\d+(?=[.]short)')
    match = assist_regex.findall(filename)[0]
    find_zero = re.compile(r'^0')
    floatable = find_zero.sub('0.',match)
    return float(floatable)


class Experiment:
    def __init__(self,yaml_config):
        # we use BaseLoader otherwise 'on' vowel is loaded as True
        with open(yaml_config) as f:
            self.config = yaml.load(f, yaml.loader.BaseLoader)

        self.vowels = self.config['Vowels']
        self.data_path = self.config['DataPath']
        self.truth_sound_files = [os.path.join(self.data_path,f'truth/{v}.wav') for v in self.vowels]
        self.sample_size = int(self.config['Sample'])
        self.trials = [Trial(n,
                             os.path.join(self.data_path,t['file']),
                             t['vowel'],
                             _get_assist(t['file']),
                             ) 
                       for n,t in enumerate(self.config['Trials'])]

    def randomize(self):
        k = min(self.sample_size, len(self))
        return [t.sort_index for t in sample(self.trials,k)]

    def __getitem__(self,n):
        return *astuple(self.trials[n]), zip(self.vowels, self.truth_sound_files)

    def __len__(self):
        return len(self.trials)

        
@dataclass(order=True)
class Trial:
    sort_index: int
    sound_file: str
    vowel: str
    assist: float
