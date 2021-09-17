# optiver-realized-volatility

## Setting up an environment

I recommend using Anaconda to manage environments. Create a new environment with

```
conda create -n optiver
```

you should then install python with `conda install python`. After you have done this you can install all the project requirements with

```
pip install -r requirements.txt
```

Make sure to add anything needed to run your notebooks to this file.

## Getting started

The competition data will need to be unzipped into a `PROJECT_ROOT/data/raw/` directory before the notebooks will function. One way to get the competition data is to download it from the [Kaggle API](https://github.com/Kaggle/kaggle-api):

```
kaggle competitions download -c optiver-realized-volatility-prediction -p data/raw/
```

After downloading the data make sure to unzip it correctly. Your project directory structure should look like this:

```
|-- data
|   |-- raw
|   |   |-- book_train.parquet
|   |   |   |-- stock_id=0
|   |   |   |-- stock_id=1
|   |   |   |-- ...
|   |   |-- book_test.parquet
|   |   |-- trade_train.parquet
|   |   |-- ...
|-- notebooks
|-- optiver
|-- README.md
|-- LICENSE
|-- ...
```

To get an idea for how to work on the project, start reading the notebooks in `notebooks/reports/`. Read them in order starting from `0.1-grchristensen-data-preparation.ipynb`. Put rough drafts and experimental notebooks in `notebooks/exploratory`, and take a look at the link explaining the project structure in "Useful Resources."

## Useful Resources

- Understanding the project structure: https://drivendata.github.io/cookiecutter-data-science/
- Handling version control with jupyter notebooks: https://www.wrighters.io/version-control-for-jupyter-notebooks/
