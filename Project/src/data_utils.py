import pandas as pd
import numpy as np
import time

def load_dict_like_text_file(file_path, BLK_SIZE=100, MAX_BLK=10000) -> pd.DataFrame:
    """
    Load a text file with key-value pairs into a dictionary.
    
    Format:

    key1: value1 \n
    key2: value2 \n
    \\n \n
    key1: value1 \n
    key2: value2 \n
    ...

    Parameters
    ----------
    file_path : str
        Path to the text file.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns 'key' and 'value'.
    """
    t_last = 0
    DISPLAY_DELAY = 0.3
    anim_index = 0
    c = ['|', '/', '-', '\\']
    filename = file_path.split('/')[-1]
    with open(file_path, 'r') as f:
        df = None
        blk_dict = dict()
        blk_list = list()
        line = f.readline()
        while line != '':
            if line == '\n':
                # Create dataframe if first time with a block
                if df is None:
                    df = pd.DataFrame([blk_dict])
                elif len(blk_list) < BLK_SIZE:
                    blk_list.append(blk_dict.copy())
                else:
                    df = pd.concat([df, pd.DataFrame(blk_list)], ignore_index=True)
                    blk_list.clear()
            else:
                values = line.strip().split(':')
                blk_dict[values[0]] = ''.join(values[1:]).strip()
            if df is not None and len(df) >= MAX_BLK:
                break
            line = f.readline()
            if time.time() - t_last > DISPLAY_DELAY:
                t_last = time.time()
                print('LOADING "{0}" {1}'.format(filename, c[anim_index % len(c)]), end='\r', flush=True)
                anim_index += 1
    print("                                                          ", end='\r')
    print("LOADED '{0}'".format(filename))
    return df