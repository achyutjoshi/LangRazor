# version 0.1

# AIM - create functions that make loading language models easy. Also validates and summarizes a new models
# All the language models goes inside the /data/language folder of the script

import json
import pandas as pd
import csv

def load_universe():
    # UNIVERSE_PATH = "data/language/language_universe.json"
    UNIVERSE_PATH = "data/language/language_universe.csv"

    try:
        universe = pd.read_csv(UNIVERSE_PATH)
        return(universe)

    except IOError:
        print("I/O Error : Check the UNIVERSE_PATH")


def append_universe(list):
    UNIVERSE_PATH = "data/language/language_universe.csv"

    try:
        with open(UNIVERSE_PATH,"a+") as f:
            write = csv.writer(f,quoting = csv.QUOTE_NONNUMERIC)
            write.writerow(list)

    except IOError:
        print("I/O Error : Check the UNIVERSE_PATH")


#model_name in the universe should be unique
def check_existance(model_name, path_return = False):
    universe = load_universe()
    if model_name in universe.model_name.values :
        if path_return == True:
            path = "data/language/" + str(universe.loc[universe.model_name == model_name].lang_id.values[0]) + "/" + str(universe.loc[universe.model_name == model_name].file_name.values[0])
            return(path)
        else:
            return(True)
    return(False)


def add_model(model_name, path,lang_id):
    universe_list = load_universe()
    append_row = [lang_id,model_name,path]
    if not check_existance(model_name):
        append_universe(append_row)
    else:
        raise ValueError(f'{model_name} already exists in language_universe')
