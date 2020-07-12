# Extrator de precedentes do STJ e STF

Esse pacote oferece uma ferramenta em Python 2.7 para a extração de citação de precedentes de decisões do Superior Tribunal de Justiça (STJ) e do Supremo Tribunal Federal (STF). Por precedentes nos referimos a citações a processos já decididos pelo tribunal.

## Installation Instructions

To install the package just clone the repository.

To install the requirements run from the package root folder:

```
pip install -r requirements.txt
```

## Running

To run the program you must have a JSON file containing a list of Paths to the decision files.

The programs take the following arguments:

```
--ids Path to JSON file containing the paths to decisions to be extracted
--court or -c STJ or STF. Court from which precedents are being extracted. This is used to infer from which court the precedent cited is in the absence of more information
--n_cores Number of processess to be executed in paralel by Python's Multiprocessing.
```

To run the program you must  run the following command from the root:

```
python core.py --ids FILE -c COURT --n_cores N_PROCESS
```
