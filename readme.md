# Bearing RUL Predict

## Installing
```
pip install -r requirements.txt
```

## Run

jupyter-notebook main.ipynb

## Analysing Code Performance - cProfile
```
python -m cProfile -o results.prof code.py
```
* You can use snakeviz to visualize the profiler results.

```
pip install snakeviz

snakeviz results.prof
```

## data folder tree organization

./data
├── original_data
    └── femto_dataset
        ├── Bearing1_1
        ├── Bearing1_2
        ├── Bearing1_3
        ├── Bearing1_4
        ├── Bearing1_5
        ├── Bearing1_6
        ├── Bearing1_7
        ├── Bearing2_1
        ├── Bearing2_2
        ├── Bearing2_3
        ├── Bearing2_4
        ├── Bearing2_5
        ├── Bearing2_6
        ├── Bearing2_7
        ├── Bearing3_1
        ├── Bearing3_2
        └── Bearing3_3

└── processed_data
    ├── Bearing1_1
    ├── Bearing1_2
    ├── Bearing1_3
    ├── Bearing1_4
    ├── Bearing1_5
    ├── Bearing1_6
    ├── Bearing1_7
    ├── Bearing2_1
    ├── Bearing2_2
    ├── Bearing2_3
    ├── Bearing2_4
    ├── Bearing2_5
    ├── Bearing2_6
    ├── Bearing2_7
    ├── Bearing3_1
    ├── Bearing3_2
    └── Bearing3_3




