<head><meta charset="utf-8"/></head>

# data-science-exercise

*Author: luphord*

## Overview

In this data science exercise, a dataset provided by the Australian Bureau of Statistics is downloaded and prepared for analysis. The time series of number of houses approved in New South Wales is then investigated, quantitatively modelled and a prediction is performed.

The analysis is performed in a series of notebooks which can be found in `notebooks/`.
These notebooks use functionality provided by the `australian_housing` Python package.
Data preparation and report generation is provided as a pipeline using `make`.

## Pipeline

The following `make` targets are useful for running this project as a pipeline:

    download            Download raw json data from Australian Bureau of Statistics 
    extract_dataframe   Decode raw json data and extract a (multidimensional) dataframe 
    extract_timeseries  Extract New South Wales housing time series 
    reports             Generate reports from jupyter notebooks


## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make download` or `make reports`
    ├── README.md          <- The top-level README for developers using this project
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed
    │   ├── processed      <- The final, canonical data sets for modeling
    │   └── raw            <- The original, immutable data dump
    │
    ├── notebooks          <- Jupyter notebooks containing the analysis and exploration.
    │
    ├── references         <- Task and data structure description.
    │
    ├── reports            <- Generated analysis as HTML, can be batched-produced using `make reports`
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so australian_housing can be imported
    └── australian_housing <- Source code for use in this project.
        ├── __main__.py    <- Entry point and CLI interface (try `python3 -m australian_housing`)
        │
        ├── data           <- Scripts, functions and classes to download, decode and extract data
        │
        └── models         <- Functions to support model building and analysis in the notebooks. No pipeline here.


--------

<p><small>This project is based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
