# Developed by Débora Rodrigues Pereira

import sys
import netCDF4 as nc
import numpy as np
from osgeo import gdal
from collections import Counter
 
def process_all_cells(future_file_path,output_path):

    future_nc_file = nc.Dataset(future_file_path, 'r')

    # Extract relevant variables
    latitudes = future_nc_file.variables['lat'][:]
    longitudes = future_nc_file.variables['lon'][:]
    #starts in 2015, every 5 years
    time_values = future_nc_file.variables['time'][:]
    print (time_values)
    veg = future_nc_file.variables['veg'][year_index][:][:]
    agric = future_nc_file.variables['agric'][year_index][:][:]
    fores = future_nc_file.variables['fores'][year_index][:][:]
    vegc = future_nc_file.variables['vegc'][year_index][:][:]
    mosc = future_nc_file.variables['mosc'][year_index][:][:]
    pastp = future_nc_file.variables['pastp'][year_index][:][:]
       
    raster = np.zeros(veg.shape)

    for i in range(veg.shape[0]):
        for j in range(veg.shape[1]):
            pveg = veg[i,j]
            pagric = agric[i,j]
            pfores = fores[i,j]
            pvegc = vegc[i,j]
            pmosc = mosc[i,j]
            ppastp = pastp[i,j]
            
            values = [pveg, pagric, pfores, pvegc, pmosc, ppastp]
            # values 
            # pveg = 1; pagric = 2; pfores = 3; pvegc = 4; pmosc = 5; ppastp = 6 
            
            total = sum(values)
            percentages = [value / total if total > 0 else 0 for value in values]

            # Find the index of the variable with the highest percentage
            predominant_index = np.argmax(percentages) + 1  # Add 1 because your classes start from 1

            # Assign the predominant vegetation type to the raster array
            raster[i, j] = predominant_index

        else:
            raster[i,j] = -99
        
#        count_minus_99 = 0
#        total_cells = 0
#        percentage_minus_99 =0
#        
#        for i in range(raster.shape[0]):
#            for j in range(raster.shape[1]):
#                if raster[i, j] == -99:
#                    count_minus_99 += 1
#                total_cells += 1
#        # Calcular a porcentagem
#            percentage_minus_99 = (count_minus_99 / total_cells) * 100
#            #print(f"Porcentagem de células com valor -99: {percentage_minus_99:.2f}%")
#
        for i in range(raster.shape[0]):
            for j in range(raster.shape[1]):
                if raster[i, j] == -99:
                    neighbors_values = []
                    adjacent_indices = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]

                    for x, y in adjacent_indices:
                        if 0 <= x < raster.shape[0] and 0 <= y < raster.shape[1] and raster[x, y] != -99:
                            neighbors_values.append(raster[x, y])

                    valid_neighbors = [value for value in neighbors_values if 1 <= value <= 6]

                    # Se todos os vizinhos são válidos, adicione as coordenadas à lista
                    if valid_neighbors:
                        most_frequent_value = max(set(valid_neighbors), key=valid_neighbors.count)
                        raster[i, j] = most_frequent_value
                              
    future_nc_file.close()   
    
    #Salvar em raster, lidar com as coordenadas
    dst_filename = output_path
    x_pixels = raster.shape[1]  # number of pixels in x
    y_pixels = raster.shape[0]  # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filename,x_pixels, y_pixels, 1,gdal.GDT_Float32)
    dataset.GetRasterBand(1).WriteArray(raster)

    # follow code is adding GeoTranform and Projection
    geotransform_0 = np.min(longitudes)
    geotransform_1 = longitudes[1]-longitudes[0] #w-e pixel resolution
    geotransform_2 = 0
    geotransform_3 = np.min(latitudes)
    geotransform_4 = 0
    geotransform_5 = -(abs(latitudes[1])-abs(latitudes[0]))#  n-s pixel resolution (negative value)
    
    dataset.SetGeoTransform([geotransform_0,geotransform_1,geotransform_2,geotransform_3,geotransform_4,geotransform_5])
    dataset.SetProjection('EPSG:4326')
    dataset.FlushCache()
    dataset=None
    
# Netcdf Path
future_file_path = 'D:/DOUTORAMENTO/LandUse/LUCCMEBR_2050/output_raster/LUCCMEBR_SSP2_RCP45_clipped.nc'
output_path = 'D:/DOUTORAMENTO/LandUse/LUCCMEBR_2050/output_raster/LUCCMEBR_SSP2_RCP45_2050_realv3.tif'
 
# Parameters:
year_index = 7

# Call the function
process_all_cells(future_file_path,output_path)
