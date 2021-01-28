# Precedent Extractor for STJ and STF

This package offers a Python 2.7 tool for the extraction of precedents citation from opinions issued by the Brazilian Superior Court of Justice (Superior Tribunal de Justiça - STJ) and Brazilian Supreme Court (Supremo Tribunal Federal - STF). 



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

## Testing

To run the full routine of tests included use the following command

```
python -m unittest discover -s test -p 'tests_*.py'
```

## Output

The file output is saved to a CSV file named out.csv. It should look like the table below.

| Documento                               | Classe | Num     | Tribunal |
|-----------------------------------------|--------|---------|----------|
| 20170526_AREsp_1035422_8421733 | resp   | 1234057 | STJ      |
| 20170526_AREsp_1035422_8421733 | resp   | 1507973 | STJ      |
| 20080502_Ag_1016162_102373     | sum\.  | 5       | STJ      |
| 20080502_Ag_1016162_102373     | sum\.  | 7       | STJ      |
| 20080502_Ag_1016162_102373     | resp   | 829835  | STJ      |
| 20080502_Ag_1016162_102373     | resp   | 208468  | STJ      |
| 20080502_Ag_1016162_102373     | eresp  | 237553  | STJ      |
| 20080502_Ag_1016162_102373     | resp   | 473159  | STJ      |


Columns translation:

  1. Documento: name of the file from which citation was extracted
  2. Classe: Cited case class, which type of proceeding was filled before the Court.
  3. Num: Number designated by the Court. With classe identifies the cited precedent from that Court
  4. Tribunal: Court from which the case was cited. Inferred by textual patterns, and by default it is the same as Court that issued the opinion.
