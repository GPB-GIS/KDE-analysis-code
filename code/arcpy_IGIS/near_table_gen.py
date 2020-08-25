# Generate point file of point with highest population
# Calculate distances between these points using Generate Near Table
# Will use this with Python notebook to join tables together and calculate Cum Pop versus Distance

# Required libraries
import arcpy
import os

arcpy.CheckOutExtension("Spatial")

# Global variables
data_path = #SET HOME PATH

# Overwrite data
arcpy.env.overwriteOutput = True

# Set workspace to folder containing  individual comms pop points
arcpy.env.workspace = data_path + "working_files/comm_pop_points.gdb/"

# List the tables in the workspace, ready for iterating over
comm_shps = arcpy.ListFeatureClasses()
#print(comm_shps)

# For each community in our list of community tables
for comm_shp in comm_shps:
    # calcuate max Comm Pro
    high_point = data_path + "working_files/comm_points_near_table.gdb/" + comm_shp + "_hp"
    stats_field = [["Comm_Pro", "MAX"]] 
    case_field = ""
    

    arcpy.Statistics_analysis(comm_shp, high_point, stats_field, case_field)

    #print(comm_shp + " processed")

    # return value of max field
    max_field = "MAX_Comm_Pro"

    cursor = arcpy.SearchCursor(high_point)
    for row in cursor:
        max_comm_pro = row.getValue(max_field)
        #print(max_comm_pro)

    # export highest point
    out_path= data_path + "working_files/comm_points_near_table.gdb/"
    query = "\"Comm_Pro\" =" + str(max_comm_pro)
    comm_cp = comm_shp + "_cp"
    arcpy.FeatureClassToFeatureClass_conversion(comm_shp, out_path, comm_cp, query)
    print(comm_shp + "cp exported")
    
    # run near table
    comm_table = data_path + "working_files/comm_tables/" + comm_shp + "_table.txt"
    search_radius = ""
    location = "LOCATION"
    angle = "ANGLE"
    closest = "ALL"
    closest_count = ""
    method ="PLANAR"

    arcpy.GenerateNearTable_analysis(out_path + comm_cp, comm_shp, comm_table, search_radius, location, angle, closest, closest_count, method)

    print(comm_shp + "table processed")
