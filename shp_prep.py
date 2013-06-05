import os
import psycopg2

shp_in = "in/shp/network-saved.shp"
table_out = "nw"
target_srid = str(4326)
db_name = "bze"
db_port = str(54321)

print "Preparing the shapefile "+shp_in+" ..."

# Loading the shapefile into the database
cmd = "shp2pgsql -W LATIN1 -d -D -I -t 2D -S -s "+target_srid+" "+shp_in+" "+table_out+" > "+table_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

# Loading the result using psql
cmd = "psql -p "+db_port+" -d "+db_name+" -f "+table_out+".sql"
print "Executing command: "+cmd
os.system(cmd)

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
	# for the snapping to work best, especially at visual intersections, we need to add the intersecting points in the original geometries
	print "Step 0"
	sql = "update "+table_out+" set geom=ST_Union("+table_out+".geom,ST_Intersection("+table_out+".geom,b.geom)) from "+table_out+" b where b.gid <> "+table_out+".gid and ST_GeometryType(ST_Union("+table_out+".geom,ST_Intersection("+table_out+".geom,b.geom)))='ST_LineString';"
	print sql
	cur.execute(sql)
	conn.commit()

	# Dropping minified table
	print "Step 1"
	sql = "DROP TABLE IF EXISTS "+table_out+"_mini CASCADE;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Recreating minified table as a grid-snapped version
	print "Step 2a"
	sql = "CREATE TABLE "+table_out+"_mini AS SELECT gid,name,geom as the_geom FROM "+table_out
	print sql
	cur.execute(sql)
	conn.commit()

	# Added PK
	print "Step 2b"
	sql = "ALTER TABLE "+table_out+"_mini ADD CONSTRAINT "+table_out+"_mini_pk PRIMARY KEY(gid);"
	print sql
	cur.execute(sql)
	conn.commit()

	# Renaming routes to ensure unicity of the name
	print "Step 2c"
	sql = "UPDATE "+table_out+"_mini SET name='R'||CAST(gid as character varying);"
	print sql
	cur.execute(sql)
	conn.commit()

	# Recreating minified table as a grid-snapped version
	print "Step 2d"
	sql = "ALTER TABLE "+table_out+"_mini ADD CONSTRAINT "+table_out+"_mini_uk UNIQUE(name);"
	print sql
	cur.execute(sql)
	conn.commit()

	# Getting the IDs (gids) and names of the routes 
	print "Step 3"
	sql = "SELECT gid,name from "+table_out+"_mini"
	print sql
	cur.execute(sql)
	rows = cur.fetchall()


	# Snapping every route to every other route - to avoid duplicate / slightly different routes along the same road (ex: other side of the road, ...)
	#exceptions = [['6','15']]
	for row in rows:
		print "Step 4x"
		sql = "UPDATE "+table_out+"_mini SET the_geom=(select ST_Snap("+table_out+"_mini.the_geom,a.the_geom,0.0001) from "+table_out+"_mini a where a.gid = "+str(row[0])+") WHERE "+table_out+"_mini.gid <> "+ str(row[0])
		print sql
		cur.execute(sql)
		conn.commit()

	# Manually re-snapping elements: [route from,route to, tolerance]
	#resnap = [['EW3-R01','NS_05_01','0.0005'],['NS_05_01','NS_05_02','0.0005'],['NS_05_03','NS_05_02','0.0005'],['EW3-R03','NS_05_03','0.0005'],['EW3-R05','NS_05_02','0.005'],['EW3-R06','NS_05_06','0.0001'],['EW3-R05','EW3-R03','0.0005'],['NS-05-07LM','NS_05_04','0.0005'],['NS-05-07LM','NS_05_02','0.0003'],['EW3-R08','EW3-R04','0.0002'],['NS_05_05','EW3-R04','0.0005']]
	#for val in resnap:
	#	print "Step 5x"
	#	sql = "UPDATE "+table_out+"_mini SET the_geom=(select ST_Snap("+table_out+"_mini.the_geom,a.the_geom,"+str(val[2])+") from "+table_out+"_mini a where a.name = '"+str(val[1])+"') where name='"+str(val[0])+"'"
	#	print sql
	#	cur.execute(sql)
	#	conn.commit()

	# Dropping minified table
	print "Step 5"
	sql = "DROP TABLE IF EXISTS "+table_out+"_inter CASCADE;"
	print sql
	cur.execute(sql)
	conn.commit()

	# Creating a point structure based on the intersections (dimension 0 intersections)
	print "Step 6"
	sql = "create table "+table_out+"_inter as select * from (select cast(nextval('"+table_out+"_gid_seq') as integer) AS id,(ST_Dump(ST_Intersection(a.the_geom,b.the_geom))).geom as the_geom from "+table_out+"_mini a, "+table_out+"_mini b where a.gid < b.gid and ST_Intersects(a.the_geom,b.the_geom)) t where st_dimension(the_geom)=0"
	print sql
	cur.execute(sql)	
	conn.commit()

	# Inserting in the point structure the intersections (dimension 1 intersections)
	print "Step 7"
	sql = "insert into "+table_out+"_inter select id,(st_dump(ST_Collect(ST_startpoint(the_geom),st_endpoint(the_geom)))).geom as the_geom from (select cast(nextval('"+table_out+"_gid_seq') as integer) AS id,(ST_Dump(ST_LineMerge(ST_Intersection(a.the_geom,b.the_geom)))).geom as the_geom from "+table_out+"_mini a, "+table_out+"_mini b where a.gid < b.gid and ST_Intersects(a.the_geom,b.the_geom)) t where st_dimension(the_geom)=1"
	print sql
	cur.execute(sql)	
	conn.commit()

	# Creating an index on it
	print "Step 10"
	sql = "CREATE INDEX "+table_out+"_mini_geom_gist ON "+table_out+"_mini USING gist (the_geom);"
	print sql
	cur.execute(sql)
	conn.commit()

except Exception,e: 
    print "I can't do that"
    print str(e)
 