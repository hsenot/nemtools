import os
import psycopg2

target_srid = "4326"
db_name = "bze"
db_port = str(54321)
ogr2ogr = "C:\\Herve\\tools\\gdal\\bin\\gdal\\apps\\ogr2ogr.exe"

table_out = ["train","tram"]

gtfs_in = {}
gtfs_in["train"] = "in/gtfs/train-20120802.zip"
gtfs_in["tram"] = "in/gtfs/tram-20120802.zip"

filename_out={}
filename_out["train"] = "from_gtfs-train"
filename_out["tram"] = "from_gtfs-tram"

shp = {}
shp["train"] = "out/"+filename_out["train"]+".shp"
shp["tram"]  = "out/"+filename_out["tram"] +".shp"

line_arr={}
line_arr["train"] = ['Alamein','Belgrave','Craigieburn','Cranbourne','Frankston','Glen Waverley','Hurstbridge','Lilydale','Pakenham','Sandringham','South Morang','Stony Point','Sydenham','Upfield','Werribee','Williamstown']
line_arr["tram"] = ['109','112','11','16','19','1','24','3-3a','30','31','35','48','55','57','59','5','64','67','6','70','72','75','78','79','82','86','8','95','96']

try:

	for mode in table_out:

		# Creating a KML file from the GTFS file
		cmd = "python gtfs/python/kmlwriter.py "+gtfs_in[mode]+" tmp/"+filename_out[mode]+".kml"
		print "Executing command: "+cmd
		#os.system(cmd)

		for line in line_arr[mode]:
			# Now translating those into shapefiles
			cmd = ogr2ogr + " -f \"ESRI Shapefile\" "+shp[mode]+" tmp/"+filename_out[mode]+".kml \"Patterns-"+str(line)+"\" -overwrite"
			print "Executing command: "+cmd
			os.system(cmd)

			# Loading the shapefile into the database
			cmd = "shp2pgsql -d -D -I -t 2D -S -s "+target_srid+" "+shp[mode]+" \""+mode+"_"+str(line)+"\" > "+mode+".sql"
			print "Executing command: "+cmd
			os.system(cmd)

			# Loading the result using psql
			cmd = "psql -p "+db_port+" -d "+db_name+" -f "+mode+".sql"
			print "Executing command: "+cmd
			os.system(cmd)

			# Loading the result using psql
			cmd = "delete "+mode+".sql"
			print "Executing command: "+cmd
			os.system(cmd)

		# Now playing with the created table
		conn_str = "dbname='"+db_name+"' user='postgres' host='localhost' port='"+db_port+"'"
		conn = psycopg2.connect(conn_str)
		if conn:
			print "Now connected to the database"

		cur = conn.cursor()

		# selecting the pattern with the most stops on each line
		print "Step 1"
		sql = "DROP TABLE IF EXISTS "+mode+" CASCADE;"
		print sql
		cur.execute(sql)
		conn.commit()
		just_dropped = True

		# Train tables loaded, now creating a single table with the most stopped pattern within each line
		for line in line_arr[mode]:
			mode_line = mode+"_"+str(line).lower()
			sql_most_complex_pattern = "SELECT CAST('"+str(line)+"' AS character varying(32)) AS name,geom AS the_geom FROM \""+mode_line+"\" ORDER BY ST_NPoints(geom) DESC LIMIT 1"

			# selecting the pattern with the most stops on each line
			print "Step 2-"+str(line)
			if just_dropped:
				sql = "CREATE TABLE "+mode+" AS "+sql_most_complex_pattern
				just_dropped = False
			else:
				sql = "INSERT INTO "+mode+" "+sql_most_complex_pattern

			print sql
			cur.execute(sql)
			conn.commit()

			# We could be deleting the pattern tables here, we don't need them anymore
			# selecting the pattern with the most stops on each line
			print "Step 3-"+str(line)
			sql = "DROP TABLE IF EXISTS \""+mode_line+"\" CASCADE;"
			print sql
			cur.execute(sql)
			conn.commit()

except Exception,e: 
    print "I can't do that"
    print str(e)
