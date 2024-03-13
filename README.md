This code was specifically written to extract information from Future Land-Use developed by Bezerra et al. (2024)

> Bezerra, F. G. S., Von Randow, C., Assis, T. O., Bezerra, K. R. A., Tejada, G., Castro, A. A., Gomes, D. M. de P., Avancini, R., & Aguiar, A. P. (2024). 
> LuccME/INLAND land-use scenarios for Brazil 2050 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10611737

First, the netcdf is clipped to the study area using a shapefile. 
Then, the script find_land_use.py is used to extract the predominant vegetation per cell,
and save this information as a Tiff file.
