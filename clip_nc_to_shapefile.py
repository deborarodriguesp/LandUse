import xarray as xr
import geopandas as gpd
from shapely.geometry import mapping

def clip_nc_to_shapefile(nc_path, shapefile_path, output_path):
    # Carregue o NetCDF
    ds = xr.open_dataset(nc_path, decode_times=False)

    # Carregue o shapefile da bacia hidrográfica
    gdf = gpd.read_file(shapefile_path)

    # Obtenha o envelope da bacia hidrográfica
    envelope = gdf.geometry.envelope
    minx, miny, maxx, maxy = envelope.total_bounds

    # Selecione apenas as células dentro do envelope
    ds_subset = ds.sel(lon=slice(minx, maxx), lat=slice(miny, maxy))

    # Converta o xarray.Dataset para um array numpy
    subset_data = ds_subset['veg'].values

    # Salve a nova versão do NetCDF (se necessário)
    ds_subset.to_netcdf(output_path)

    # Feche os datasets
    ds.close()
    ds_subset.close()
    
 # Netcdf Path
nc_path  = 'D:/DOUTORAMENTO/LandUse/LUCCMEBR_2050/LUCCMEBR_SSP2_RCP45_land_cover_type_100km2-2015-2050.nc'

# Watershed shapefile:
shapefile_path = 'D:/DOUTORAMENTO/LandUse/LUCCMEBR_2050/LandUseAnalisys/BaciaTAW/baciatocantis_araguaia.shp'

# Output Path for the Clipped NetCDF
output_path = 'D:/DOUTORAMENTO/LandUse/LUCCMEBR_2050/output_raster/LUCCMEBR_SSP2_RCP45_clipped.nc'

clip_nc_to_shapefile(nc_path, shapefile_path, output_path)