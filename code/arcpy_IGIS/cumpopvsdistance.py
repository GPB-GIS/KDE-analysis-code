# Script to join NEAR TABLE output to Comm Points with population

# Display Near Table XY using Near X and Near Y
# Spatial Join Near Table to Comm Points with Population
# Clean files (using field mapping option in join)

## Required libraries
import arcpy
import os

arcpy.CheckOutExtension("Spatial")

# Global variables
data_path = #SET HOME PATH

# Overwrite data
arcpy.env.overwriteOutput = True

# Set workspace to folder containing  individual comms tables
arcpy.env.workspace = data_path + "working_files/comm_pop_points.gdb/"

# List the tables in the workspace, ready for iterating over
comm_shps = arcpy.ListFeatureClasses()
#print(comm_shps)

# For each community in our list of community tables
for comm_shp in comm_shps:
    print(comm_shp)

    # display x and y of comm_table of same community
    comm_table = data_path + "working_files/comm_tables/" + comm_shp + "_table.txt"
    x_field = "NEAR_X"
    y_field = "NEAR_Y"
    comm_nt_points_temp = comm_shp + "_temp"
    comm_nt_points = data_path + "working_files/comm_tables/" + comm_shp + "_points.shp"

    CRS = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision"

    arcpy.MakeXYEventLayer_management(comm_table, x_field, y_field, comm_nt_points_temp, CRS)

    arcpy.CopyFeatures_management(comm_nt_points_temp, comm_nt_points)

    print(comm_shp + ": Points layer created")

    # spatial join of data
    comm_export = data_path + "working_files/comm_distpop/" + comm_shp + ".shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    match_option = "ARE_IDENTICAL_TO"

    ## Create our list of fields using the Field Mapping objects

    fieldmappings = arcpy.FieldMappings()

    ### Add all fields from our two datasets
    fieldmappings.addTable(comm_shp)
    fieldmappings.addTable(comm_nt_points)
    
    ### Create a list of the fields that we want in our final shapefile, southampton_lsoas_crime
    fields_to_keep = ["FID", "Total_Pop", "Pro_Pop", "Comm_Pro", "NEAR_FID", "NEAR_DIST", "NEAR_RANK", "NEAR_ANGLE"]

    ### Remove any fields in our field mappings that are not in our fields_to_keep list
    for field in fieldmappings.fields:
        if field.name not in fields_to_keep:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

    fields_to_join = fieldmappings

    arcpy.SpatialJoin_analysis(comm_shp, comm_nt_points, comm_export, join_operation, join_type, fields_to_join, match_option)

    print(comm_shp + ": Spatial join complete")
##    
## Follow with ipynb Communtiy Distance versus Population Comparison to create dataset
## That dataset caculates a cumulative population based on distance
##
    
