import os
import psycopg2

shp_in = "in/network_sample.shp"
table_out = "nw_sample"
target_srid = str(4326)
db_name = "bze"
db_port = str(54321)

print "Preparing the shapefile "+shp_in+" ..."

# Loading the shapefile into the database
cmd = "shp2pgsql -d -D -I -t 2D -S -s "+target_srid+" "+shp_in+" "+table_out+" > "+table_out+".sql"
print "Executing command: "+cmd
#os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_out+".sql"
print "Executing command: "+cmd
#os.system(cmd)

# Now playing with the created table
try:
	conn_str = "dbname='"+db_name+"' user='postgres' host='localhost' port='"+db_port+"'"
	conn = psycopg2.connect(conn_str)
	if conn:
		print "Now connected to the database"
		# Keeping only the bare minimum table: gid and geom
except:
    print "I am unable to connect to the database"

cur = conn.cursor()
try:
	# Dropping minified table
	print "Step 1"
	sql = "DROP TABLE IF EXISTS "+table_out+"_mini CASCADE;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Recreating minified table
	print "Step 2"
	sql = "CREATE TABLE "+table_out+"_mini AS SELECT gid,geom as the_geom FROM "+table_out
	print sql
	cur.execute(sql)
	conn.commit()

	# Truncating it
	print "Step 3"
	sql = "TRUNCATE TABLE "+table_out+"_mini"
	print sql
	cur.execute(sql)	
	conn.commit()

	# Now, the fun begins - let's cut the spaghetti

	# Determining intersection points
	# Using an interative algorithm, considering all existing segments one after the other (loop)
	# If it's got (point) intersections with any other segment, then it needs to be split
	# We remove the initial segment and insert the split part(s)

	# Do we need to repeat? It seems that by construction, we're going to find all intersections in one pass, TBC

	# Creating an index on it
	print "Step 10"
	sql = "CREATE INDEX "+table_out+"_mini_geom_gist ON "+table_out+"_mini USING gist (the_geom);"
	print sql
	cur.execute(sql)
	conn.commit()

except:
    print "I can't do that"    