# Required libraries
import arcpy
import os

arcpy.CheckOutExtension("Spatial")

# Global variables
data_path = #SET HOME PATH

# Overwrite data
arcpy.env.overwriteOutput = True

# Set workspace to folder containing  individual comms tables
arcpy.env.workspace = data_path + "raw/ind_comm/"

# List the tables in the workspace, ready for iterating over
comm_files = arcpy.ListFiles()
print(comm_files)

# For each community in our list of community tables
for comm_file in comm_files[43]:
    
    # isolate community name
    comm_shp = comm_file.split('.')[0]
    print(comm_shp)
    print(comm_file)

    # display xy of the community
    x_field = "lon"
    y_field = "lat"
    CRS = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision"

    # call this comm_poins
    comm_points = arcpy.MakeXYEventLayer_management(comm_file, x_field, y_field, comm_shp, CRS)
    comm_points_file = data_path + "working_files/comm_points/" + comm_shp + ".shp"
    arcpy.CopyFeatures_management(comm_points, comm_points_file)

    print(comm_shp + ' XY displayed!')

    # join this with the 11 district voronoi shp

    ## set path to voronoi shp file

    voronoi_pop_grid = data_path + 'raw/AOI_11_THIESSEN_CLIP.shp'

    ## set parameters, join operation, join type, match option

    community_voronoi = data_path + "working_files/comm_pop_voronois/" + comm_shp + ".shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_COMMON"
    match_option = "CONTAINS"

    ## set fields to join

    fieldmappings = arcpy.FieldMappings()

    ### Add all fields from our two datasets
    fieldmappings.addTable(voronoi_pop_grid)
    fieldmappings.addTable(comm_points_file)

    ### Create a list of the fields that we want in our final shapefile, southampton_lsoas_crime
    fields_to_keep = ["OBJECTID", "community", "count"]

    ### Remove any fields in our field mappings that are not in our fields_to_keep list
    for field in fieldmappings.fields:
        if field.name not in fields_to_keep:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))


    fields_to_join = fieldmappings

    ## run join function

    arcpy.SpatialJoin_analysis(voronoi_pop_grid, comm_points_file, community_voronoi, join_operation, join_type, fields_to_join, match_option)

    # then join this 11 district population grid shp

    ## set path to population grid shp file
    pop_grid = data_path + "working_files/comm_vor_pop_grid.shp"

    ## set parameters, join operation, join type, match option
    community_wpopulation = data_path + "working_files/community_wpopulation/" + comm_shp + "_pop.shp"

    match_option2 = "WITHIN"

    ## set fields to join

    fieldmappings2 = arcpy.FieldMappings()

    ### Add all fields from our two datasets
    fieldmappings.addTable(pop_grid)
    fieldmappings.addTable(community_voronoi)

    ### Create a list of the fields that we want in our final shapefile(s)
    fields_to_keep = ["Total_Pop", "Pro_Pop", "OBJECTID", "community", "count"]

    ### Remove any fields in our field mappings that are not in our fields_to_keep list
    for field in fieldmappings.fields:
        if field.name not in fields_to_keep:
            fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

    fields_to_join2 = fieldmappings2

    ## run join function

    arcpy.SpatialJoin_analysis(pop_grid, community_voronoi, community_wpopulation, join_operation, join_type, fields_to_join2, match_option2)

    # Add community members proportion field
                               
    comm_pro_field = "Comm_Pro"
    field_type = "DOUBLE"

    arcpy.AddField_management(community_wpopulation, comm_pro_field, field_type)

    # Calculate members per grid square

    calculation = "(!Pro_Pop! * !count!)"
    expression_type = "PYTHON"

    arcpy.CalculateField_management(community_wpopulation, comm_pro_field, calculation, expression_type)

    print(comm_shp + " file processing complete")
