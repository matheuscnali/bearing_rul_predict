# Bearing RUL Predict

## Installing required packages.
```
pip install -r requirements.txt
```

## Organizing data folder.
This project expects a data folder in root with the following structure:

```
.
├── Bearing-RUL-Predict
    ├── data
        ├── original_data
        │   ├── dataset1
        |   |   ├── Bearing1
        |   |   |   ├── file1.csv      
        |   |   |   ├── file2.csv
        |   |   |   ├── ...
        |   |   ├── Bearing2
        |   |   |   ├── file1.csv      
        |   |   |   ├── file2.csv
        |   |   ├── ...
        │   ├── dataset2
        |   |   ├── Bearing1
        |   |   |   ├── ...
        |   |   ├── Bearing2
        |   |   |   ├── ...
        |   |   ├── ...
        │   └── ...
        └── processed_data
```

## Run
```
jupyter-notebook main.ipynb
```
## Analysing Code Performance - cProfile
```
python -m cProfile -o results.prof code.py
```
* You can use snakeviz to visualize the profiler results.

```
pip install snakeviz

snakeviz results.prof
```

## Some results using FEMTO dataset.
<img src="docs/images/all_bearings_results.png"
     alt="All femto dataset bearings results"/>

