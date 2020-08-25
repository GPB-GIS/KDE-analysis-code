# Generating KDE coverage maps from gridded community polygons

# Required libraries
import arcpy
import os

arcpy.CheckOutExtension("Spatial")

# Global variables
data_path = #SET HOME PATH

# Overwrite data
arcpy.env.overwriteOutput = True

# Set workspace to folder containing  individual comms tables
arcpy.env.workspace = data_path + "comm_pop_points.gdb/"

# List all datasets within comm pop folder

comm_datasets = arcpy.ListFeatureClasses()

#print(comm_datasets)

for comm_dataset in comm_datasets[32:33]:
    print(comm_dataset)

    comm_pop_points_1person =  data_path + "comm_pop_points_1person/" + comm_dataset + ".shp"
    selection_query = "\"Comm_Pro\" >= 1"
    
    arcpy.Select_analysis(comm_dataset, comm_pop_points_1person, selection_query)

    # run KDE on points file
    pop_field = "Comm_Pro"
    comm_kde = data_path + "kde_1person.gdb/" + comm_dataset
    cell_size = "0.0039"
    bandwidth = "0.015"
    scale_factor = "SQUARE_MAP_UNITS"
    kde_unit = "EXPECTED_COUNTS"
    distance ="PLANAR"

    arcpy.env.extent = "C:/Users/jowilkin/Documents/PhD/ssc/data/raw/AOI_11_districts.shp"
  
    arcpy.gp.KernelDensity_sa(comm_pop_points_1person, pop_field, comm_kde, cell_size, bandwidth, scale_factor, kde_unit, distance)

    print(comm_dataset + " kde created")

print("Processing Complete!")
