## Installation

If you get any error when installing cartopy and/or shapely, execute the following command in your terminal:
```
sudo apt install libgeos-dev libproj-dev proj-data proj-bin libbz2-dev libblas3 liblapack3 liblapack-dev libblas-dev libatlas-base-dev gfortran
```


## Running

```
reset && python3 -B -m simulator -d "inmet_2020_south" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 12 -n 5 -a "knn" && python3 -B -m simulator -d "inmet_2020_south" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 12 -n 5 -a "idw" && python3 -B -m simulator -d "inmet_2020_south" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 12 -n 5 -a "first_fit_proposal" && python3 -B -m simulator -d "inmet_2020_south" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 12 -n 5 -a "proposed_heuristic"
```


## References

- https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.LinearNDInterpolator.html
- https://www.inf.usi.ch/hormann/papers/Hormann.2014.BI.pdf
- https://github.com/scipy/scipy/blob/17e6c0e9223e619a3b65d4ddf8b77ee9c0bd1614/scipy/interpolate/interpnd.pyx
- https://github.com/pmav99/interpolation
- https://en.wikipedia.org/wiki/Multivariate_interpolation
- https://stackoverflow.com/questions/64881351/python-geospatial-interpolation-meteorological-data
