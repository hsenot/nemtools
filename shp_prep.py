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

	# Recreating minified table as a grid-snapped version
	print "Step 2"
	sql = "CREATE TABLE "+table_out+"_mini AS SELECT gid,geom as the_geom FROM "+table_out
	print sql
	cur.execute(sql)
	conn.commit()

	# Getting the IDs (gids) of the 
	print "Step 3"
	sql = "SELECT gid from "+table_out+"_mini"
	print sql
	cur.execute(sql)
	rows = cur.fetchall()

	# Snapping every route to every other route - to avoid duplicate / slightly different routes along the same road (ex: other side of the road, ...)
	exceptions = [['6','15']]
	for row in rows:
		print "Step 4x"
		sql = "UPDATE "+table_out+"_mini SET the_geom=(select ST_Snap("+table_out+"_mini.the_geom,a.the_geom,0.00011) from "+table_out+"_mini a where a.gid = "+str(row[0])+")"
		print sql
		cur.execute(sql)
		conn.commit()

	# Manual re-snapping
	resnap = [['13','2','0.0005'],['2','5','0.0005'],['4','5','0.0005'],['15','4','0.0005'],['16','5','0.005'],['17','6','0.0001'],['16','15','0.0005'],['7','1','0.0005'],['7','5','0.0003'],['10','9','0.0002'],['3','9','0.0005']]
	for val in resnap:
		print "Step 5x"
		sql = "UPDATE "+table_out+"_mini SET the_geom=(select ST_Snap("+table_out+"_mini.the_geom,a.the_geom,"+str(val[2])+") from "+table_out+"_mini a where a.gid = "+str(val[1])+") where gid="+str(val[0])
		print sql
		cur.execute(sql)
		conn.commit()


	# Dropping minified table
	print "Step 5"
	sql = "DROP TABLE IF EXISTS "+table_out+"_inter CASCADE;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Creating a point structure based on the intersections - dimension 0 intersections
	print "Step 6"
	sql = "create table "+table_out+"_inter as select * from (select cast(nextval('"+table_out+"_gid_seq') as integer) AS id,(ST_Dump(ST_Intersection(a.the_geom,b.the_geom))).geom as the_geom from "+table_out+"_mini a, "+table_out+"_mini b where a.gid < b.gid and ST_Intersects(a.the_geom,b.the_geom)) t where st_dimension(the_geom)=0"
	print sql
	cur.execute(sql)	
	conn.commit()

	# Inserting in the point structure the intersections - dimension 1 intersections
	print "Step 7"
	sql = "insert into "+table_out+"_inter select id,(st_dump(ST_Collect(ST_startpoint(the_geom),st_endpoint(the_geom)))).geom as the_geom from (select cast(nextval('"+table_out+"_gid_seq') as integer) AS id,(ST_Dump(ST_LineMerge(ST_Intersection(a.the_geom,b.the_geom)))).geom as the_geom from "+table_out+"_mini a, "+table_out+"_mini b where a.gid < b.gid and ST_Intersects(a.the_geom,b.the_geom)) t where st_dimension(the_geom)=1"
	print sql
	cur.execute(sql)	
	conn.commit()


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