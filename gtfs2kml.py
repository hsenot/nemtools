import os
import psycopg2

gtfs_in = "in/gtfs/train-20120802.zip"
filename_out = "shp_from_gtfs-train"

gtfs2_in = "in/gtfs/tram-20120802.zip"
filename2_out = "shp_from_gtfs-tram"

try:
	# Creating a KML file from the GTFS file
	cmd = "python gtfs/python/kmlwriter.py "+gtfs_in+" tmp/"+filename_out+".kml"
	print "Executing command: "+cmd
	os.system(cmd)

	# Creating a KML file from the GTFS file
	cmd = "python gtfs/python/kmlwriter.py "+gtfs2_in+" tmp/"+filename2_out+".kml"
	print "Executing command: "+cmd
	os.system(cmd)

except:
    print "I can't do that"    