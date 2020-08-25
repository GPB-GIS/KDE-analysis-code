# Reclassify KDE rasters into 40% coverage maps

# import required libraies
import os
import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")

# overwrite datasets
arcpy.env.overwriteOutput = True

# set path to datasets
data_path = #SET HOME PATH

# set workspace to loop through
arcpy.env.workspace = data_path + "kde_1person.gdb/"

# list rasters in workspace
kde_data = arcpy.ListRasters()

print(kde_data)

# Loop through each raster
for raster in kde_data:
    comm_nm = raster
    print(comm_nm)

    raster_Max = arcpy.GetRasterProperties_management (raster, "MAXIMUM")
    raster_Max_no = float(raster_Max.getOutput(0))
    print(raster_Max_no)

    percent = 0.40 * raster_Max_no
    print(percent)

    # Reclassify raster
    field = "VALUE"
    reclassify_values = "0 " + str(percent) + " 1;" + str(percent) + " " + str(raster_Max_no) + " 2"
    missing_values = "NODATA"
    print(reclassify_values)

    output_raster = Reclassify(raster, field, reclassify_values, missing_values)

    output_raster.save(data_path + "reclassified_kdes_40/" + comm_nm)

    print(comm_nm + " processed")

print("Processing Complete")

 
