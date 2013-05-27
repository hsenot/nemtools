import os
import psycopg2

gtfs_in = "in/gtfs/train-20120802.zip"
filename_out = "shp_from_gtfs-train"
target_srid = str(4326)

# Now playing with the created table
try:
	# Creating a KML file from the GTFS file
	cmd = "python gtfs/python/kmlwriter.py "+gtfs_in+" tmp/"+filename_out+".kml"
	print "Executing command: "+cmd
	os.system(cmd)

except:
    print "I can't do that"    