# Pull any base image that includes python3
FROM python:3.12

# install the toolbox runner tools
RUN pip install json2args==0.6.1

# install pandas and pandas-profiling
RUN pip install pandas==2.1.4 ydata-profiling==4.7.0 pyarrow==15.0.0

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["python", "run.py"]