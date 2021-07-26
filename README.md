## Installation

If you get any error when installing cartopy and/or shapely, execute the following command in your terminal:
```
sudo apt install libgeos-dev libproj-dev proj-data proj-bin
```


## Running

```
python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)" -t 24 -s 24 -a "idw" -o "topo1.png" && python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)" -t 24 -s 24 -a "knn" -o "topo1.png" && python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)" -t 24 -s 24 -a "first_fit_proposal" -o "topo1.png" && python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)" -t 24 -s 24 -a "proposed_heuristic" -o "topo1.png"
```


## References

- https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.LinearNDInterpolator.html
- https://www.inf.usi.ch/hormann/papers/Hormann.2014.BI.pdf
- https://github.com/scipy/scipy/blob/17e6c0e9223e619a3b65d4ddf8b77ee9c0bd1614/scipy/interpolate/interpnd.pyx
- https://github.com/pmav99/interpolation
- https://en.wikipedia.org/wiki/Multivariate_interpolation
- https://stackoverflow.com/questions/64881351/python-geospatial-interpolation-meteorological-data
