import json
import os
from glob import glob
import pandas as pd
import numpy as np

expected_files = sorted(glob('expected_output/*/*.json'))

if len(expected_files) < 24:
    raise ValueError('Expected 24 files, but only %d files exist' % len(expected_files))

output_files = sorted(glob('output/*/*.json'))

if len(output_files) != len(expected_files):
    print('Mismatch in number of expected (%d) and actual (%d) output files' % (len(expected_files),
                                                                                len(output_files)))

df = pd.DataFrame()
for filename in expected_files:
    with open(filename, 'rt') as fp:
        in_dict = json.load(fp)
        subject = filename.split(os.path.sep)[1]
        in_dict_mod = {}
        for k, v in in_dict.items():
            if isinstance(v, list):
                for idx, value in enumerate(v):
                    in_dict_mod["k%d" % idx] = value
            else:
                in_dict_mod[k] = v
        df[subject] = pd.Series(in_dict_mod)
df = df.T

df_out = pd.DataFrame()
for filename in output_files:
    with open(filename, 'rt') as fp:
        in_dict = json.load(fp)
        subject = filename.split(os.path.sep)[1]
        in_dict_mod = {}
        for k, v in in_dict.items():
            if isinstance(v, list):
                for idx, value in enumerate(v):
                    in_dict_mod["k%d" % idx] = value
            else:
                in_dict_mod[k] = v
        df_out[subject] = pd.Series(in_dict_mod)
df_out = df_out.T

if np.allclose(df, df_out):
    print('Outputs are close enough!')
else:
    print('Outputs are not close enough. Printing difference')
    print(df - df_out)

    