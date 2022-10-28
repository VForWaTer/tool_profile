# Dataset profiler

This repository contains a docker image for generating statistical dataset reportsin  HTML and JSON using standardized input and outputs. This is based on the template for a generic containerized Python [tool](https://github.com/vforwater/tool_template_python).

## How standardized?

Tools using this template can be run by the [toolbox-runner](https://github.com/hydrocode-de/tool-runner). 
That is only convenience, the tools implemented using this template are independent of any framework.

The main idea is to implement a common file structure inside container to load inputs and outputs of the 
tool. The template shares this structures with the [R template](https://github.com/vforwater/tool_template_r)
and [Octave template](https://github.com/vforwater(tool_template_octave), but can be mimiced in any container.

Each container needs at least the following structure:

```
/
|- in/
|  |- tool.json
|- out/
|  |- ...
|- src/
|  |- tool.yml
|  |- run.py
```

* `tool.json` are parameters. Whichever framework runs the container, this is how parameters are passed.
* `tool.yml` is the tool specification. It contains metadata about the scope of the tool, the number of endpoints (functions) and their parameters
* `run.py` is the tool itself, or a Python script that handles the execution. It has to capture all outputs and either `print` them to console or create files in `/out`

## How to build the image?

You can build the image from within the root of this repo by
```
docker build -t tbr_profile .
```

Use any tag you like. If you want to run and manage the container with [toolbox-runner](https://github.com/hydrocode-de/tool-runner)
they should be prefixed by `tbr_` to be recognized. 

Alternatively, the contained `.github/workflows/docker-image.yml` will build the image for you 
on new releases on Github. You need to change the target repository in the aforementioned yaml and the repository needs a 
[personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
in the repository secrets in order to run properly.

## How to run?

This template installs the toolbox-runner python package to parse the parameters in the `/in/tool.json`. This assumes that
the files are not renamed and not moved and there is actually only one tool in the container. For any other case, the environment variables
`PARAM_FILE` can be used to specify a new location for the `tool.json` and `TOOL_RUN` can be used to specify the tool to be executed.
The `run.py` has to take care of that.

To invoke the docker container directly run something similar to:
```
docker run --rm -it -v /path/to/local/in:/in -v /path/to/local/out:/out -e TOOL_RUN=profile tbr_profile
```

Then, the output will be in your local out and based on your local input folder. Stdout and Stderr are also connected to the host.

With the toolbox runner, this is simplyfied:

```python
import pandas as pd
from toolbox_runner import list_tools
tools = list_tools() # dict with tool names as keys

prof= tools.get('profile') 

# load any pdatas Dataframe
df = pd.read_csv('mydata.csv')
res = foobar.run(result_path='./', data=df)

# now, there is a tar.gz with all outputs
print(res)  # giving you the path

# but you can also export the JSON report
import json
json.loads(res.get_file('./out/report.json'),decode())

```
The example above will create a temporary file structure to be mounted into the container and then create a `.tar.gz` on termination of all 
inputs, outputs, specifications and some metadata, including the image sha256 used to create the output in the current working directory.

## What's included
Currently, only variogram estimation using SciKit-GStat and kriging using GSTools is implemented. Simulations and parameter grid search are on the agenda.

You can learn about the available tools and their parameters directly from the container:
```
docker run --rm -it tbr_profile bash cat /srv/tool.yml
```
or using toolbox runner

```python
from toolbox_runner import list_tools
tools = list_tools() # dict with tool names as keys

prof = tools.get('profile')
prof.title
prof.description
prof.parameters
```
