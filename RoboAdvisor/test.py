import pandas as pd
from ast import literal_eval
import json
from script import Script

if __name__ == '__main__':
    
    Script_handler = Script()
    # print(Script_handler.Q_set)
    print(Script_handler.Q_set.iloc[0]['judgement'])
    print(type(Script_handler.Q_set.iloc[0]['judgement']))