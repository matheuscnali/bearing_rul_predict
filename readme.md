# Bearing RUL Predict

## Installing
```
pip install -r requirements.txt
```

## To run
```
python main.py
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

