import sys
import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import arcpy
import time

config = ConfigParser.ConfigParser()
config.read('config.cfg')
fc = config.get('field_to_mosaic','input_layer')

field = "Name" #field name with raster

field_value = []
n_count = 0

cursor = arcpy.SearchCursor(fc)
row = cursor.next()
while row:
     field_value.append(str(row.getValue(field)))
     row = cursor.next()
     n_count +=1 
#print field_value

rasters = []

for item in field_value:
    
    rasterLayerName = str(item) + '.img' 
    rasterPath = "D:\LiDAR_DEM\\"+ rasterLayerName +";"  #raster path
    rasters.append(os.path.join(rasterPath))
    
ras_list = ';'.join(rasters)    
    
print ('The number of read imagery is '+ str(n_count)+'.')


    
def main():
    ##==================================
    ##Mosaic To New Raster
    ##Usage: MosaicToNewRaster_management inputs;inputs... output_location raster_dataset_name_with_extension
    ##                                    {coordinate_system_for_the_raster} 8_BIT_UNSIGNED | 1_BIT | 2_BIT | 4_BIT
    ##                                    | 8_BIT_SIGNED | 16_BIT_UNSIGNED | 16_BIT_SIGNED | 32_BIT_FLOAT | 32_BIT_UNSIGNED
    ##                                    | 32_BIT_SIGNED | | 64_BIT {cellsize} number_of_bands {LAST | FIRST | BLEND  | MEAN
    ##                                    | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH}

    #arcpy.MosaicToNewRaster_management("landsatb4a.tif;landsatb4b.tif","Mosaic2New", "landsat.tif", "World_Mercator.prj","8_BIT_UNSIGNED", "40", "1", "LAST","FIRST")

    print time.strftime("%m-%d %X",time.localtime())+ " Start mosaicing. This may take a while."
    
    #rasters = parse_rasters_from_file('files.txt')

    pixel_type = config.get('field_to_mosaic', 'pixel_type')
    output_location = config.get('field_to_mosaic', 'output_location')
    output_dataset = config.get('field_to_mosaic', 'output_dataset')
    mosaic_method = config.get('field_to_mosaic', 'mosaic_method')
    mosaic_colormap_mode = config.get('field_to_mosaic', 'mosaic_colormap_mode')

    desc = arcpy.Describe(rasterPath.split(';')[0])
    band_count = desc.bandCount

    
    
    #spatial_reference = desc.spatialReference
    #arcpy.env.outputCoordinateSystem = spatial_reference

    arcpy.MosaicToNewRaster_management(ras_list, output_location, output_dataset, None, pixel_type, None, band_count, mosaic_method, mosaic_colormap_mode)

    print time.strftime("%m-%d %X",time.localtime())+ " Mosaic done!"
    print str (output_dataset) + " is generated."

if __name__ == '__main__':
    main()
