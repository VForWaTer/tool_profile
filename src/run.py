import os
from datetime import datetime as dt

from pandas_profiling import ProfileReport
import numpy as np
import pandas as pd

from json2args import get_parameter

# parse parameters
kwargs = get_parameter()

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'profile').lower()


def load_data(df_or_path):
    if isinstance(df_or_path, str):
        # oi
        path = kwargs['data']
        _, ext = os.path.splitext(path)

        # check some endings
        if ext.lower() in ('.xls', '.xlsx', '.odf', '.ods'):
            data = pd.read_excel(df_or_path)
        elif ext.lower() in ('.asc', '.dat', '.mat', '.txt'):
            data = pd.read_table(df_or_path, comment='#')
        else:
            raise AttributeError('Got a file path, but the extension is not (yet) supported.')
    elif isinstance(df_or_path, (np.ndarray, pd.Series)):
        data = pd.DataFrame(df_or_path)
    elif isinstance(df_or_path, pd.DataFrame):
        data = df_or_path
    else:
        raise AttributeError(f"The passed data was of type {type(df_or_path)} which is not supported.")
    return data


# switch the tool
if toolname == 'profile':
    # kwargs data will automatically be loaded as a Dataframe. If it is still a string, try
    # to figure out what this is.
    df = load_data(kwargs['data'])
    del kwargs['data']

    profile = ProfileReport(df, title="Dataset Report")

    # generate the output
    profile.to_file('/out/report.html')
    js = profile.to_json()

    with open('/out/report.json', 'w') as f:
        f.write(js)    


# In any other case, it was not clear which tool to run
else:
    with open('/out/error.log', 'w') as f:
        f.write(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
