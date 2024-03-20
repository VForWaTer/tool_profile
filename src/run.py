import os
from datetime import datetime as dt
from pathlib import Path

from ydata_profiling import ProfileReport
import pandas as pd

from json2args import get_parameter
from json2args.data import get_data_paths

# parse parameters
parameter = get_parameter()

# check if a toolname was set in env
toolname = os.environ.get('TOOL_RUN', 'profile').lower()


def load_data():
    # get the paths
    data_paths = get_data_paths()
    
    # extract the dataframe path
    df_path = data_paths['dataframe']

    # check the extension
    ext = Path(df_path).suffix.lower()

    if ext == '.csv':
        data = pd.read_csv(df_path)
    elif ext == '.parquet':
        data = pd.read_parquet(df_path)

    return Path(df_path).stem, data


# switch the tool
if toolname == 'profile':
    # kwargs data will automatically be loaded as a Dataframe. If it is still a string, try
    # to figure out what this is.
    name, df = load_data()
    

    profile = ProfileReport(
        df,
        title=parameter.get('title', "Dataset Report"),
        dark_mode=parameter['dark_mode'],
        tsmode=parameter['has_timeseries'],
    )

    # generate the output
    profile.to_file(f"/out/{name}_report.html")
    js = profile.to_json()

    with open(f"/out/{name}_report.json", 'w') as f:
        f.write(js)    


# In any other case, it was not clear which tool to run
else:
    with open('/out/error.log', 'w') as f:
        f.write(f"[{dt.now().isocalendar()}] Either no TOOL_RUN environment variable available, or '{toolname}' is not valid.\n")
